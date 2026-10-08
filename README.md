# gus-instagram-photos

Photos for [@mrgusthewondercat](https://instagram.com/mrgusthewondercat), Oct 2026 – Jan 2027.

- `photos/`: original photos (1080x1350), named as in the calendar sheet's "Photo file" column.
- `photos_with_text/`: the same photos with a text overlay, one per calendar post: `post-NNN_<photo>.jpg`.
- `scripts/overlay_lines.tsv`: the overlay line for each post (post #, top/bottom placement, lines split by `|`).
- `scripts/add_text.py`: regenerates `photos_with_text/` from the calendar CSV and the Anton font.
