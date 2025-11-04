#!/bin/sh
set -e

# Create upload directories if they don't exist
mkdir -p uploads/gallery/thumbs
mkdir -p uploads/testimonials
mkdir -p uploads/themes

alembic upgrade head
# Execute the main command
exec "$@"
