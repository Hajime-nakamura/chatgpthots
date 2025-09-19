from flask import Blueprint, jsonify, request
from .config import Config
from .services.rag import RagService

bp = Blueprint("api", __name__)
rag = RagService(dim=Config.VECTOR_DIM, max_corpus=Config.MAX_CORPUS)

@bp.route("/healthz", methods=["GET"])
def healthz():
    return jsonify({"status": "ok", "app": Config.APP_NAME})

# ---- Tools: 社内ツール連携の最小例 -----------------------
@bp.route("/v1/tools/echo", methods=["POST"])
def tool_echo():
    payload = request.get_json(silent=True) or {}
    return jsonify({"ok": True, "echo": payload})

# ---- Minimal RAG API -----------------------------------
@bp.route("/v1/rag/ingest", methods=["POST"])
def rag_ingest():
    data = request.get_json(silent=True) or {}
    items = data.get("items", [])
    if not items:
        return jsonify({"ok": False, "error": "items required"}), 400
    rag.ingest(items)
    return jsonify({"ok": True, "ingested": len(items)})

@bp.route("/v1/rag/query", methods=["POST"])
def rag_query():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "")
    top_k = int(data.get("top_k", 5))
    if not query:
        return jsonify({"ok": False, "error": "query required"}), 400
    results = rag.query(query, top_k=top_k)
    return jsonify({"ok": True, "results": results})
