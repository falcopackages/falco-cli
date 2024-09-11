# List all available commands
_default:
    @just --list

@install:
    hatch run python --version

# Install dependencies
@bootstrap:
    hatch env create
    hatch env create docs

@clean:
    hatch env prune

# Ugrade dependencies
upgrade:
    hatch run hatch-pip-compile --upgrade --all

# Run sphinx autobuild
@docs-serve:
    hatch run docs:sphinx-autobuild docs docs/_build/html --port 8002

# Generate demo project
generate-demo *OVERWRITE:
    #!/usr/bin/env bash
    set -euo pipefail
    [[ "{{ OVERWRITE }}" == "--overwrite" ]] && rm -rf demo/myjourney
    [[ -d demo/myjourney ]] && { echo "Directory demo/myjourney already exists. Use --overwrite to recreate it."; exit 0; }
    hatch run falco start-project myjourney demo -b blueprints/tailwind
    cd demo/myjourney
    just bootstrap
    just falco start-app entries
    cp ../../docs/_static/snippets/entry_model.py myjourney/entries/models.py
    just mm && just migrate
    just falco crud entries.entry --skip-git-check

# Generate documents assets
generate-docs-assets: generate-demo
    just tree
    cp demo/myjourney/myjourney/entries/urls.py docs/_static/snippets/urls.py

# Generate project tree files
tree: generate-demo
    #!/usr/bin/env bash
    set -euo pipefail
    levels=(1 2 3)
    SED_CMD=$( [[ "$OSTYPE" == "darwin"* ]] && echo "sed -i ''" || echo "sed -i" )
    for level in "${levels[@]}"; do
      tree "demo/myjourney" -L $level --dirsfirst -o tree.txt --noreport -a -n -v -I '.env|requirements*|__pycache__|entries'
      $SED_CMD 's|{{{{ cookiecutter.project_name }}|demo|g' tree.txt
      $SED_CMD 's|demo/myjourney|myjourney|g' tree.txt
      mv tree.txt docs/_static/snippets/tree-$level.txt
    done
    rm -f tree.txt\'\'

@test:
    hatch run pytest

# Run all formatters
@fmt:
    just --fmt --unstable
    hatch fmt --formatter
    hatch run pyproject-fmt pyproject.toml
    hatch run pre-commit run reorder-python-imports -a

# Bump project version and update changelog
@bumpver version:
    hatch run bump-my-version bump {{ version }}
    git push
    git push --tags

# ----------------------------------------------------------------------
# Blueprints
# ----------------------------------------------------------------------

# Initialze / update submodules
submodule-init:
    git submodule update --init --recursive

# Checkout all submodules on main
checkout:
    #!/usr/bin/env sh
    for parent_dir in blueprints; do
      for dir in $parent_dir/*; do
        if [ -d "$dir" ]; then
          echo "$(basename $dir)"
          cd "$dir"
          git checkout main
          cd -
        fi
      done
    done

# Run git pull in all submodules
pull:
    #!/usr/bin/env sh
    git pull
    for parent_dir in blueprints; do
      for dir in $parent_dir/*; do
        if [ -d "$dir" ]; then
          echo "$(basename $dir)"
          cd "$dir"
          git pull
          cd -
        fi
      done
    done

# Run git fetch in all submodules
fetch:
    #!/usr/bin/env sh
    git fetch --all
    for parent_dir in blueprints; do
      for dir in $parent_dir/*; do
        if [ -d "$dir" ]; then
          echo "$(basename $dir)"
          cd "$dir"
          git fetch --all
          cd -
        fi
      done
    done

# Set the upstream remote for alternative blueprints
set-remote:
    cd blueprints/bootstrap
    git remote add upstream "git@github.com:Tobi-De/falco_tailwind.git"

# Merge change from the upstream in all blueprints
merge:
    cd blueprints/bootstrap
    git fetch upstream
    git merge upstream/main

# Push all changes in all submodules
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
