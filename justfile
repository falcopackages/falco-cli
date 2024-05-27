default := "blueprints/falco_blueprint_basic"

# List all available commands
_default:
    @just --list

just default:
    cd {{ default }}

# Run git pull in every blueprints
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

# Set the upstream remote
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
