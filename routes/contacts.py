from flask import Blueprint, request, jsonify
from models import db, Contact
from utils.validators import validate_contact_payload
import logging
import csv
import io

contacts_bp = Blueprint("contacts", __name__)
logger = logging.getLogger(__name__)


# ── GET /api/contacts ─────────────────────────────────────────────────────────
@contacts_bp.route("/contacts", methods=["GET"])
def get_contacts():
    try:
        query = Contact.query

        # Search
        q = request.args.get("q", "").strip()
        if q:
            like = f"%{q}%"
            query = query.filter(
                db.or_(
                    Contact.first_name.ilike(like),
                    Contact.last_name.ilike(like),
                    Contact.email.ilike(like),
                    Contact.company.ilike(like),
                )
            )

        # Filter by category
        category = request.args.get("category", "").strip()
        if category and category != "all":
            if category == "favourite":
                query = query.filter(Contact.is_favorite == True)
            else:
                query = query.filter(Contact.category == category)

        # Sort
        sort = request.args.get("sort", "name")
        if sort == "recent":
            query = query.order_by(Contact.created_at.desc())
        else:
            query = query.order_by(Contact.first_name.asc(), Contact.last_name.asc())

        contacts = query.all()
        return jsonify([c.to_dict() for c in contacts]), 200

    except Exception as e:
        logger.error(f"GET /contacts error: {e}")
        return jsonify({"error": "Failed to fetch contacts."}), 500


# ── POST /api/contacts ────────────────────────────────────────────────────────
@contacts_bp.route("/contacts", methods=["POST"])
def create_contact():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided."}), 400

        errors = validate_contact_payload(data)
        if errors:
            return jsonify({"errors": errors}), 422

        # Duplicate email check
        if Contact.query.filter_by(email=data["email"].strip().lower()).first():
            return jsonify({"error": "A contact with this email already exists."}), 409

        contact = Contact(
            first_name  = data["firstName"].strip().title(),
            last_name   = data["lastName"].strip().title(),
            email       = data["email"].strip().lower(),
            phone       = data.get("phone", "").strip(),
            company     = data.get("company", "").strip(),
            address     = data.get("address", "").strip(),
            category    = data.get("category", "personal"),
            notes       = data.get("notes", "").strip(),
            is_favorite = bool(data.get("favourite", False)),
        )
        db.session.add(contact)
        db.session.commit()
        logger.info(f"Contact created: {contact.email}")
        return jsonify(contact.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"POST /contacts error: {e}")
        return jsonify({"error": "Failed to create contact."}), 500


# ── PUT /api/contacts/<id> ────────────────────────────────────────────────────
@contacts_bp.route("/contacts/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    try:
        contact = Contact.query.get(contact_id)
        if not contact:
            return jsonify({"error": "Contact not found."}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided."}), 400

        errors = validate_contact_payload(data)
        if errors:
            return jsonify({"errors": errors}), 422

        # Duplicate email check (exclude self)
        existing = Contact.query.filter_by(email=data["email"].strip().lower()).first()
        if existing and existing.id != contact_id:
            return jsonify({"error": "Another contact already uses this email."}), 409

        contact.first_name  = data["firstName"].strip().title()
        contact.last_name   = data["lastName"].strip().title()
        contact.email       = data["email"].strip().lower()
        contact.phone       = data.get("phone", "").strip()
        contact.company     = data.get("company", "").strip()
        contact.address     = data.get("address", "").strip()
        contact.category    = data.get("category", contact.category)
        contact.notes       = data.get("notes", "").strip()
        contact.is_favorite = bool(data.get("favourite", contact.is_favorite))

        db.session.commit()
        logger.info(f"Contact updated: {contact.email}")
        return jsonify(contact.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"PUT /contacts/{contact_id} error: {e}")
        return jsonify({"error": "Failed to update contact."}), 500


# ── PATCH /api/contacts/<id>/favourite ───────────────────────────────────────
@contacts_bp.route("/contacts/<int:contact_id>/favourite", methods=["PATCH"])
def toggle_favourite(contact_id):
    try:
        contact = Contact.query.get(contact_id)
        if not contact:
            return jsonify({"error": "Contact not found."}), 404
        contact.is_favorite = not contact.is_favorite
        db.session.commit()
        return jsonify(contact.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"PATCH favourite error: {e}")
        return jsonify({"error": "Failed to toggle favourite."}), 500


# ── DELETE /api/contacts/<id> ─────────────────────────────────────────────────
@contacts_bp.route("/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    try:
        contact = Contact.query.get(contact_id)
        if not contact:
            return jsonify({"error": "Contact not found."}), 404
        db.session.delete(contact)
        db.session.commit()
        logger.info(f"Contact deleted: id={contact_id}")
        return jsonify({"message": "Contact deleted."}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"DELETE /contacts/{contact_id} error: {e}")
        return jsonify({"error": "Failed to delete contact."}), 500


# ── GET /api/contacts/export ──────────────────────────────────────────────────
@contacts_bp.route("/contacts/export", methods=["GET"])
def export_csv():
    try:
        contacts = Contact.query.order_by(Contact.first_name).all()
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            "id", "first_name", "last_name", "email", "phone",
            "company", "address", "category", "notes", "is_favorite", "created_at"
        ])
        writer.writeheader()
        for c in contacts:
            writer.writerow({
                "id": c.id, "first_name": c.first_name, "last_name": c.last_name,
                "email": c.email, "phone": c.phone, "company": c.company,
                "address": c.address, "category": c.category, "notes": c.notes,
                "is_favorite": c.is_favorite, "created_at": c.created_at.isoformat()
            })
        output.seek(0)
        from flask import Response
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=contacts.csv"}
        )
    except Exception as e:
        logger.error(f"Export error: {e}")
        return jsonify({"error": "Export failed."}), 500


# ── GET /api/stats ────────────────────────────────────────────────────────────
@contacts_bp.route("/stats", methods=["GET"])
def get_stats():
    try:
        return jsonify({
            "total":    Contact.query.count(),
            "favourite": Contact.query.filter_by(is_favorite=True).count(),
            "work":     Contact.query.filter_by(category="work").count(),
            "personal": Contact.query.filter_by(category="personal").count(),
            "family":   Contact.query.filter_by(category="family").count(),
        }), 200
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return jsonify({"error": "Failed to fetch stats."}), 500
