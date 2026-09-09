# Created: 2026-09-09 14:55 JST
# Updated: 2026-09-09 14:55 JST
"""Compatibility wrapper adding click/tap zoom to article images.

The existing diagram injector remains the reviewed core. This wrapper adds one
accessible lightbox behavior to feature images, editorial inline images and the
approved explanatory diagrams. Product-card images and decorative site images
are intentionally excluded.
"""

from __future__ import annotations

import re

try:  # package import used by tests/finalizer imports
    from . import article_diagrams_core as _core
    from .article_diagrams_core import *  # noqa: F401,F403
except ImportError:  # direct import when scripts/ is on sys.path
    import article_diagrams_core as _core
    from article_diagrams_core import *  # type: ignore # noqa: F401,F403


IMAGE_ZOOM_STYLE = r"""
<style data-article-image-zoom-style>
.article-feature-image img,.article-inline-image img,.article-explainer--image img{cursor:zoom-in}
.article-feature-image img:focus-visible,.article-inline-image img:focus-visible,.article-explainer--image img:focus-visible{outline:3px solid rgba(23,107,104,.35);outline-offset:4px}
.article-image-zoom{width:min(96vw,1280px);max-width:none;padding:0;border:0;border-radius:14px;background:#101820;color:#fff;box-shadow:0 18px 60px rgba(0,0,0,.38)}
.article-image-zoom::backdrop{background:rgba(5,12,18,.82)}
.article-image-zoom__inner{position:relative;padding:46px 14px 14px}
.article-image-zoom__image{display:block;max-width:calc(96vw - 28px);max-height:82vh;width:auto;height:auto;margin:auto;object-fit:contain;background:#fff}
.article-image-zoom__caption{max-width:900px;margin:10px auto 0;color:#e8edf1;font-size:.86rem;line-height:1.6;text-align:center}
.article-image-zoom__close{position:absolute;top:8px;right:10px;min-width:38px;min-height:38px;border:1px solid rgba(255,255,255,.45);border-radius:999px;background:#fff;color:#182630;font-size:1.3rem;font-weight:800;cursor:pointer}
@media(max-width:600px){.article-image-zoom{width:100vw;border-radius:0}.article-image-zoom__inner{padding-left:8px;padding-right:8px}.article-image-zoom__image{max-width:calc(100vw - 16px);max-height:80vh}}
</style>
""".strip()

IMAGE_ZOOM_SCRIPT = r"""
<script data-article-image-zoom-script>
(function(){
  'use strict';
  var selector='.article-feature-image img, .article-inline-image img, .article-explainer--image img';
  function init(){
    var images=Array.prototype.slice.call(document.querySelectorAll(selector)).filter(function(img){return !img.closest('a');});
    if(!images.length)return;
    images.forEach(function(img){
      img.setAttribute('tabindex','0');
      img.setAttribute('role','button');
      img.setAttribute('aria-label','画像を拡大表示: '+(img.getAttribute('alt')||'記事画像'));
    });
    function openImage(img){
      var src=img.currentSrc||img.src;
      if(!src)return;
      if(typeof HTMLDialogElement==='undefined'){
        window.open(src,'_blank','noopener');
        return;
      }
      var dialog=document.getElementById('article-image-zoom-dialog');
      if(!dialog){
        dialog=document.createElement('dialog');
        dialog.id='article-image-zoom-dialog';
        dialog.className='article-image-zoom';
        dialog.setAttribute('aria-label','画像の拡大表示');
        dialog.innerHTML='<div class="article-image-zoom__inner"><button type="button" class="article-image-zoom__close" aria-label="拡大画像を閉じる">×</button><img class="article-image-zoom__image" alt=""><p class="article-image-zoom__caption"></p></div>';
        document.body.appendChild(dialog);
        dialog.querySelector('.article-image-zoom__close').addEventListener('click',function(){dialog.close();});
        dialog.addEventListener('click',function(event){if(event.target===dialog)dialog.close();});
      }
      var enlarged=dialog.querySelector('.article-image-zoom__image');
      var caption=dialog.querySelector('.article-image-zoom__caption');
      enlarged.src=src;
      enlarged.alt=img.getAttribute('alt')||'';
      var figure=img.closest('figure');
      var figcaption=figure&&figure.querySelector('figcaption');
      caption.textContent=figcaption?figcaption.textContent.trim():(img.getAttribute('alt')||'');
      dialog.showModal();
    }
    images.forEach(function(img){
      img.addEventListener('click',function(){openImage(img);});
      img.addEventListener('keydown',function(event){
        if(event.key==='Enter'||event.key===' '){event.preventDefault();openImage(img);}
      });
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
}());
</script>
""".strip()


def inject_article_image_zoom(document: str) -> str:
    """Inject the zoom behavior once when an eligible article image is present."""
    if "data-article-image-zoom-script" in document:
        return document
    if not re.search(
        r'class=["\'][^"\']*(?:article-feature-image|article-inline-image|article-explainer--image)',
        document,
        re.IGNORECASE,
    ):
        return document
    if "</head>" not in document.lower() or "</body>" not in document.lower():
        return document
    document = re.sub(r"</head>", lambda _: IMAGE_ZOOM_STYLE + "\n</head>", document, count=1, flags=re.IGNORECASE)
    document = re.sub(r"</body>", lambda _: IMAGE_ZOOM_SCRIPT + "\n</body>", document, count=1, flags=re.IGNORECASE)
    return document


def inject_article_diagram(document: str, output_path: str) -> str:
    """Run the reviewed diagram injector, then enable zoom on eligible images."""
    return inject_article_image_zoom(_core.inject_article_diagram(document, output_path))
