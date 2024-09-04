default := "blueprints/falco_tailwind"

# List all available commands
_default:
    @just --list


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

# Checkout all blueprints on main
checkout:
    #!/usr/bin/env sh
    for dir in blueprints/*; do
      if [ -d "$dir" ]; then
        echo "$(basename $dir)"
        cd "$dir"
        git checkout main
        cd -
      fi
    done

# Run git pull in all blueprints
pull:
    #!/usr/bin/env sh
    git pull
    for dir in blueprints/*; do
      if [ -d "$dir" ]; then
        echo "$(basename $dir)"
        cd "$dir"
        git pull
        cd -
      fi
    done

# Run git fetch in all blueprints
fetch:
    #!/usr/bin/env sh
    for dir in blueprints/*; do
      if [ -d "$dir" ]; then
        echo "$(basename $dir)"
        cd "$dir"
        git fetch --all
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
        git remote add upstream "git@github.com:Tobi-De/falco_tailwind.git"
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

# Publish falco to pypi
@publish:
    hatch build
    hatch publish

tree:
  #!/usr/bin/env bash
  levels=(1 2 3)
  SED_CMD=$( [[ "$OSTYPE" == "darwin"* ]] && echo "sed -i ''" || echo "sed -i" )
  for level in "${levels[@]}"; do
    tree "blueprints/tailwind/{{{{ cookiecutter.project_name }}" -L $level --dirsfirst -o tree.txt --noreport -a -n
    $SED_CMD 's|blueprints/tailwind/||g' tree.txt
    $SED_CMD 's|{{{{ cookiecutter.project_name }}|demo|g' tree.txt
    mv tree.txt docs/images/tree-$level.txt
  done
