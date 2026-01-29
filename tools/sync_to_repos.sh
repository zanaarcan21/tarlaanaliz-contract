#!/usr/bin/env bash
#
# TarlaAnaliz Contracts Sync Tool
# Syncs contracts to consumer repositories (platform, edge, worker)
# Validates hash integrity after sync
#
# Usage:
#   ./tools/sync_to_repos.sh --target platform
#   ./tools/sync_to_repos.sh --target edge --verify-only
#   ./tools/sync_to_repos.sh --all
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTRACTS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Logging
log_info() { echo -e "${BLUE}ℹ${NC} $1"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠${NC} $1"; }

# Read expected checksum from CONTRACTS_VERSION.md
get_expected_checksum() {
    local version_file="$CONTRACTS_DIR/CONTRACTS_VERSION.md"
    
    if [ ! -f "$version_file" ]; then
        log_error "CONTRACTS_VERSION.md not found"
        return 1
    fi
    
    # Extract checksum
    local checksum=$(grep -oP 'Contracts Checksum \(SHA-256\):\*\* `\K[a-f0-9]{64}' "$version_file")
    
    if [ -z "$checksum" ]; then
        log_error "Could not parse checksum from CONTRACTS_VERSION.md"
        return 1
    fi
    
    echo "$checksum"
}

# Compute actual checksum
compute_actual_checksum() {
    local temp_file=$(mktemp)
    
    # Collect all schema file hashes
    find "$CONTRACTS_DIR/schemas" -name "*.json" -type f -print0 | \
        sort -z | \
        while IFS= read -r -d '' file; do
            local rel_path="${file#$CONTRACTS_DIR/}"
            local hash=$(sha256sum "$file" | awk '{print $1}')
            echo "$rel_path:$hash" >> "$temp_file"
        done
    
    # Collect API file hashes
    find "$CONTRACTS_DIR/api" -name "*.yaml" -type f -print0 | \
        sort -z | \
        while IFS= read -r -d '' file; do
            local rel_path="${file#$CONTRACTS_DIR/}"
            local hash=$(sha256sum "$file" | awk '{print $1}')
            echo "$rel_path:$hash" >> "$temp_file"
        done
    
    # Compute combined hash
    local combined_hash=$(sha256sum "$temp_file" | awk '{print $1}')
    rm -f "$temp_file"
    
    echo "$combined_hash"
}

# Verify checksums
verify_checksums() {
    log_info "Verifying contracts checksums..."
    
    local expected=$(get_expected_checksum)
    local actual=$(compute_actual_checksum)
    
    if [ "$expected" == "$actual" ]; then
        log_success "Checksums match: $actual"
        return 0
    else
        log_error "Checksum mismatch!"
        log_error "  Expected: $expected"
        log_error "  Actual:   $actual"
        return 1
    fi
}

# Sync to platform repository
sync_to_platform() {
    local platform_dir="$1"
    log_info "Syncing to platform repository: $platform_dir"
    
    # Validate platform repo structure
    if [ ! -d "$platform_dir/.git" ]; then
        log_error "Not a git repository: $platform_dir"
        return 1
    fi
    
    local contracts_target="$platform_dir/contracts"
    
    # Create contracts directory if not exists
    mkdir -p "$contracts_target"
    
    # Sync schemas (platform needs all schemas)
    log_info "Syncing schemas..."
    rsync -av --delete \
        --exclude='*.md' \
        --exclude='examples/' \
        "$CONTRACTS_DIR/schemas/" \
        "$contracts_target/schemas/"
    
    # Sync API specs (platform needs public + internal APIs)
    log_info "Syncing API specs..."
    rsync -av \
        "$CONTRACTS_DIR/api/platform_public.v1.yaml" \
        "$CONTRACTS_DIR/api/platform_internal.v1.yaml" \
        "$CONTRACTS_DIR/api/components/" \
        "$contracts_target/api/"
    
    # Copy version file
    cp "$CONTRACTS_DIR/CONTRACTS_VERSION.md" "$contracts_target/"
    
    # Generate types for platform
    log_info "Generating TypeScript types for platform..."
    (cd "$CONTRACTS_DIR" && ./tools/generate_types.sh --typescript)
    
    if [ -d "$CONTRACTS_DIR/generated/typescript" ]; then
        rsync -av "$CONTRACTS_DIR/generated/typescript/" "$platform_dir/src/types/contracts/"
    fi
    
    log_success "Synced to platform repository"
}

# Sync to edge repository
sync_to_edge() {
    local edge_dir="$1"
    log_info "Syncing to edge repository: $edge_dir"
    
    if [ ! -d "$edge_dir/.git" ]; then
        log_error "Not a git repository: $edge_dir"
        return 1
    fi
    
    local contracts_target="$edge_dir/contracts"
    mkdir -p "$contracts_target"
    
    # Edge needs: edge schemas, intake, quarantine, metadata
    log_info "Syncing edge-specific schemas..."
    
    mkdir -p "$contracts_target/schemas/edge"
    mkdir -p "$contracts_target/schemas/shared"
    mkdir -p "$contracts_target/schemas/enums"
    
    # Sync required schemas only
    rsync -av "$CONTRACTS_DIR/schemas/edge/" "$contracts_target/schemas/edge/"
    rsync -av "$CONTRACTS_DIR/schemas/shared/" "$contracts_target/schemas/shared/"
    rsync -av \
        "$CONTRACTS_DIR/schemas/enums/threat_type.enum.v1.json" \
        "$CONTRACTS_DIR/schemas/enums/quarantine_decision.enum.v1.json" \
        "$contracts_target/schemas/enums/"
    
    # Sync edge API
    log_info "Syncing edge API spec..."
    rsync -av \
        "$CONTRACTS_DIR/api/edge_local.v1.yaml" \
        "$CONTRACTS_DIR/api/components/" \
        "$contracts_target/api/"
    
    # Copy version file
    cp "$CONTRACTS_DIR/CONTRACTS_VERSION.md" "$contracts_target/"
    
    # Generate Python types for edge
    log_info "Generating Python types for edge..."
    (cd "$CONTRACTS_DIR" && ./tools/generate_types.sh --python)
    
    if [ -d "$CONTRACTS_DIR/generated/python" ]; then
        rsync -av "$CONTRACTS_DIR/generated/python/" "$edge_dir/src/contracts/"
    fi
    
    log_success "Synced to edge repository"
}

# Sync to worker repository
sync_to_worker() {
    local worker_dir="$1"
    log_info "Syncing to worker repository: $worker_dir"
    
    if [ ! -d "$worker_dir/.git" ]; then
        log_error "Not a git repository: $worker_dir"
        return 1
    fi
    
    local contracts_target="$worker_dir/contracts"
    mkdir -p "$contracts_target"
    
    # Worker needs: worker schemas, analysis job/result, enums
    log_info "Syncing worker-specific schemas..."
    
    mkdir -p "$contracts_target/schemas/worker"
    mkdir -p "$contracts_target/schemas/shared"
    mkdir -p "$contracts_target/schemas/enums"
    
    # Sync required schemas
    rsync -av "$CONTRACTS_DIR/schemas/worker/" "$contracts_target/schemas/worker/"
    rsync -av "$CONTRACTS_DIR/schemas/shared/geojson.v1.schema.json" "$contracts_target/schemas/shared/"
    rsync -av \
        "$CONTRACTS_DIR/schemas/enums/crop_type.enum.v1.json" \
        "$CONTRACTS_DIR/schemas/enums/analysis_type.enum.v1.json" \
        "$contracts_target/schemas/enums/"
    
    # Copy version file
    cp "$CONTRACTS_DIR/CONTRACTS_VERSION.md" "$contracts_target/"
    
    # Generate Python types for worker
    log_info "Generating Python types for worker..."
    (cd "$CONTRACTS_DIR" && ./tools/generate_types.sh --python)
    
    if [ -d "$CONTRACTS_DIR/generated/python" ]; then
        rsync -av "$CONTRACTS_DIR/generated/python/" "$worker_dir/src/contracts/"
    fi
    
    log_success "Synced to worker repository"
}

# Create sync commit
create_sync_commit() {
    local target_dir="$1"
    local target_name="$2"
    
    log_info "Creating sync commit in $target_name..."
    
    cd "$target_dir"
    
    # Check if there are changes
    if ! git diff --quiet || ! git diff --cached --quiet; then
        # Get version from contracts
        local version=$(grep -oP 'Version: \K[0-9]+\.[0-9]+\.[0-9]+' "$target_dir/contracts/CONTRACTS_VERSION.md" | head -1)
        
        # Stage changes
        git add contracts/
        git add src/types/contracts/ 2>/dev/null || true
        git add src/contracts/ 2>/dev/null || true
        
        # Create commit
        git commit -m "chore: sync contracts to v${version}

Synced from tarlaanaliz-contracts@${version}
Checksum: $(get_expected_checksum)

This is an automated sync of contract schemas and types."
        
        log_success "Created sync commit"
        log_info "To push changes: cd $target_dir && git push"
    else
        log_info "No changes to commit"
    fi
}

# Main function
main() {
    echo ""
    log_info "TarlaAnaliz Contracts Sync Tool"
    echo ""
    
    local target=""
    local verify_only=false
    local auto_commit=false
    local sync_all=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --target)
                target="$2"
                shift 2
                ;;
            --verify-only)
                verify_only=true
                shift
                ;;
            --auto-commit)
                auto_commit=true
                shift
                ;;
            --all)
                sync_all=true
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --target <platform|edge|worker>  Sync to specific target"
                echo "  --all                             Sync to all targets"
                echo "  --verify-only                     Only verify checksums"
                echo "  --auto-commit                     Auto-commit changes in target repo"
                echo "  --help, -h                        Show this help"
                echo ""
                echo "Environment variables:"
                echo "  PLATFORM_DIR   Path to platform repository"
                echo "  EDGE_DIR       Path to edge repository"
                echo "  WORKER_DIR     Path to worker repository"
                echo ""
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Verify checksums first
    if ! verify_checksums; then
        log_error "Checksum verification failed!"
        log_error "Please run: python3 tools/pin_version.py --verify"
        exit 1
    fi
    
    if [ "$verify_only" = true ]; then
        log_success "Verification complete"
        exit 0
    fi
    
    # Sync to targets
    if [ "$sync_all" = true ]; then
        # Sync to all targets
        if [ -n "${PLATFORM_DIR:-}" ]; then
            sync_to_platform "$PLATFORM_DIR"
            [ "$auto_commit" = true ] && create_sync_commit "$PLATFORM_DIR" "platform"
        fi
        
        if [ -n "${EDGE_DIR:-}" ]; then
            sync_to_edge "$EDGE_DIR"
            [ "$auto_commit" = true ] && create_sync_commit "$EDGE_DIR" "edge"
        fi
        
        if [ -n "${WORKER_DIR:-}" ]; then
            sync_to_worker "$WORKER_DIR"
            [ "$auto_commit" = true ] && create_sync_commit "$WORKER_DIR" "worker"
        fi
    elif [ -n "$target" ]; then
        # Sync to specific target
        case $target in
            platform)
                if [ -z "${PLATFORM_DIR:-}" ]; then
                    log_error "PLATFORM_DIR environment variable not set"
                    exit 1
                fi
                sync_to_platform "$PLATFORM_DIR"
                [ "$auto_commit" = true ] && create_sync_commit "$PLATFORM_DIR" "platform"
                ;;
            edge)
                if [ -z "${EDGE_DIR:-}" ]; then
                    log_error "EDGE_DIR environment variable not set"
                    exit 1
                fi
                sync_to_edge "$EDGE_DIR"
                [ "$auto_commit" = true ] && create_sync_commit "$EDGE_DIR" "edge"
                ;;
            worker)
                if [ -z "${WORKER_DIR:-}" ]; then
                    log_error "WORKER_DIR environment variable not set"
                    exit 1
                fi
                sync_to_worker "$WORKER_DIR"
                [ "$auto_commit" = true ] && create_sync_commit "$WORKER_DIR" "worker"
                ;;
            *)
                log_error "Invalid target: $target"
                log_error "Valid targets: platform, edge, worker"
                exit 1
                ;;
        esac
    else
        log_error "No target specified"
        log_info "Use --target <platform|edge|worker> or --all"
        exit 1
    fi
    
    echo ""
    log_success "Sync complete!"
    echo ""
}

# Run main
main "$@"