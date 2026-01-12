from __future__ import annotations

from pathlib import Path

import sass
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Compila SCSS para static/css/custom.css (Bootstrap 5 + overrides)."

    def handle(self, *args, **options):
        static_dir = Path(settings.BASE_DIR) / "static"
        src = static_dir / "scss" / "custom.scss"
        dst = static_dir / "css" / "custom.css"

        if not src.exists():
            raise CommandError(f"SCSS source não encontrado: {src}")

        dst.parent.mkdir(parents=True, exist_ok=True)
        css = sass.compile(filename=str(src), output_style="compressed")
        dst.write_text(css, encoding="utf-8")

        self.stdout.write(self.style.SUCCESS(f"SCSS compilado: {src} -> {dst}"))
