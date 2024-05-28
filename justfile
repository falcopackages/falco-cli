default := "blueprints/falco_blueprint_basic"

# List all available commands
_default:
    @just --list

# ----------------------------------------------------------------------
# Blueprints
# ----------------------------------------------------------------------

# Initialze / update submodules
init:
    git submodule update --init --recursive

# Run git pull in all blueprints
pull:
    #!/usr/bin/env sh
    for dir in blueprints/*; do
      if [ -d "$dir" ]; then
        echo "$(basename $dir)"
        cd "$dir"
        git fetch --all
        git pull
        cd -
      fi
    done

# Set the upstream remote for alternative blueprints
set-remote:
    #!/usr/bin/env sh
    for dir in blueprints/*; do
      if [ -d "$dir" ]; then
        if [ "$dir" = "{{ default }}" ]; then
          continue
        fi
        echo "$(basename $dir)"
        cd "$dir"
        git remote add upstream "git@github.com:Tobi-De/falco_blueprint_basic.git"
        cd -
      fi
    done

# Merge change from the upstream in all blueprints
merge:
    #!/usr/bin/env sh
    for dir in blueprints/*; do
      if [ -d "$dir" ]; then
        if [ "$dir" = "{{ default }}" ]; then
          continue
        fi
        echo "$(basename $dir)"
        cd "$dir"
        git merge upstream/main
        cd -
      fi
    done

# Push all changes in all blueprints
push:
    #!/usr/bin/env sh
    for dir in blueprints/*; do
      if [ -d "$dir" ]; then
        echo "$(basename $dir)"
        cd "$dir"
        git pull
        git push
        cd -
      fi
    done

# ----------------------------------------------------------------------
# UTILS
# ----------------------------------------------------------------------

# CD into the default blueprint folder
@just default:
    cd {{ default }}

# Run all formatters
@fmt:
    just --fmt --unstable

# Bump project version and update changelog
@bumpver version:
    just cmd bump-my-version bump {{ version }}
    git push
    git push --tags

@publish:
    hatch build
    hatch publish
