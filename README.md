# XPONEXUS Portfolio

This repository hosts the XPONEXUS structural engineering portfolio on GitHub Pages.

## One-time website upload

Upload the supplied `XPO Portfolio - Dynamic Watermark.html` to the repository root and rename it to `index.html`.

GitHub's browser uploader accepts this file size. Once `index.html` exists, the included GitHub Actions workflow will automatically deploy the site.

## Add a new PDF project

Upload project PDFs to `/pdfs/` using this filename format:

`CLIENT__PROJECT TITLE__CATEGORY.pdf`

Example:

`John Smith__25 Example Road__Rear extension.pdf`

Optionally upload a preview image to `/previews/` with the same filename stem:

`John Smith__25 Example Road__Rear extension.jpg`

After the commit, GitHub Actions scans `/pdfs/`, regenerates `portfolio-projects.json`, and redeploys the portfolio. No HTML editing is required.

## Optional project metadata

For custom descriptions, add a JSON file beside the PDF with the same filename stem:

```json
{
  "context": "Rear extension and internal structural alterations.",
  "scope": "Structural drawings, steelwork and construction details.",
  "sheetCount": 8
}
```

## Watermark

The website viewer overlays:

`PROPERTY OF XPONEXUS • CLIENT NAME`

The client name is taken from the first part of the PDF filename.

## GitHub Pages

After `index.html` has been uploaded:

1. Open **Settings → Pages**.
2. Under **Build and deployment**, choose **GitHub Actions** as the source if it is not already selected.
3. Open the **Actions** tab and confirm **Build and deploy XPONEXUS portfolio** completes successfully.

The public site will be available at:

`https://igrisarise223-web.github.io/xponexus-portfolio/`

## Security note

The watermark and hidden browser toolbar are deterrents rather than DRM. Any public PDF delivered to a visitor's browser can ultimately be captured by a determined user.
