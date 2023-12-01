#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from openj.db import get_db

card = Blueprint("card", __name__, url_prefix="/api")


@card.post("/card")
def create_card():
    """Create card."""

    form = request.form.copy().to_dict()
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            """
            INSERT INTO card (
                title,
                description,
                lane_id
            ) VALUES (
                :title,
                :description,
                :lane_id
            )
            """,
            form,
        )
        db.commit()
    except db.ProgrammingError:
        return "Missing parameter(s).", 400
    except db.IntegrityError:
        return "Invalid parameter(s).", 400
    return "Card successfully created.", 201


@card.get("/card/<int:id>")
def read_card(id: int):
    """Read card."""

    row = (
        get_db()
        .execute(
            "SELECT * FROM card WHERE id = ?",
            (id,),
        )
        .fetchone()
    )
    if not row:
        return "Card does not exist.", 404
    return dict(row), 200


@card.put("/card/<int:id>")
def update_card(id: int):
    """Update card."""

    form = request.form.copy().to_dict()
    form["id"] = id
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            """
            UPDATE card SET
                updated_at = CURRENT_TIMESTAMP,
                title = :title,
                description = :description,
                lane_id = :lane_id
            WHERE id = :id
            """,
            form,
        )
        db.commit()
    except db.ProgrammingError:
        return "Missing parameter(s).", 400
    except db.IntegrityError:
        return "Invalid parameter(s).", 400
    return "Card successfully updated.", 201


@card.delete("/card/<int:id>")
def delete_card(id: int):
    """Delete card."""

    db = get_db()
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("DELETE FROM card WHERE id = ?", (id,))
    db.commit()
    return "Card successfully deleted.", 200


@card.get("/card")
def list_cards():
    """List cards."""

    rows = get_db().execute("SELECT * FROM card").fetchall()
    if not rows:
        return "Cards do not exist.", 404
    return list(map(dict, rows)), 200
