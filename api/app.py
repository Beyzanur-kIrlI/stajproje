from flask import Flask, request, jsonify
from .extensions import db, migrate
from .models import Job, JobResult
from .tasks import run_shell_command_task, run_katana_task
from .config import Config
from datetime import datetime
import uuid

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprints yükle
    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Tasks import burada (circular import'u engellemek için)
    from . import tasks

    @app.route("/jobs", methods=["POST"])
    def create_job():
        data = request.json or {}
        job_type = data.get("job_type")
        name = data.get("name") or f"{job_type}-{uuid.uuid4().hex[:6]}"
        params = data.get("params", {})

        if job_type not in ("shell", "katana"):
            return jsonify({"error": "unsupported job_type"}), 400

        job = Job(name=name, job_type=job_type, params=params)
        db.session.add(job)
        db.session.commit()

        result = JobResult(job_id=job.id, status="pending")
        db.session.add(result)
        db.session.commit()

        # Görevleri Celery ile çalıştır
        if job_type == "shell":
            run_shell_command_task.delay(job.id, result.id)
        elif job_type == "katana":
            run_katana_task.delay(job.id, result.id)

        return jsonify({"job_id": job.id, "result_id": result.id}), 201

    @app.route("/jobs", methods=["GET"])
    def list_jobs():
        jobs = Job.query.order_by(Job.created_at.desc()).all()
        return jsonify([
            {
                "id": j.id,
                "name": j.name,
                "job_type": j.job_type,
                "created_at": j.created_at.isoformat(),
                "results": [{"id": r.id, "status": r.status} for r in j.results]
            } for j in jobs
        ])

    @app.route("/results/<int:result_id>", methods=["GET"])
    def get_result(result_id):
        r = JobResult.query.get_or_404(result_id)
        return jsonify({
            "id": r.id,
            "job_id": r.job_id,
            "status": r.status,
            "output": r.output,
            "meta": r.meta,
            "created_at": r.created_at.isoformat(),
            "finished_at": r.finished_at.isoformat() if r.finished_at else None
        })

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)

