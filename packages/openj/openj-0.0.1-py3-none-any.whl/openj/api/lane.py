#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from openj.db import get_db

lane = Blueprint("lane", __name__, url_prefix="/api")


@lane.post("/lane")
def create_lane():
    """Create lane."""

    form = request.form.copy().to_dict()
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            """
            INSERT INTO lane (
                title,
                slug
            ) VALUES (
                :title,
                :slug
            )
            """,
            form,
        )
        db.commit()
    except db.ProgrammingError:
        return "Missing parameter(s).", 400
    except db.IntegrityError:
        return "Invalid parameter(s).", 400
    return "Lane successfully created.", 201


@lane.get("/lane/<int:id>")
def read_lane(id: int):
    """Read lane."""

    row = (
        get_db()
        .execute(
            "SELECT * FROM lane WHERE id = ?",
            (id,),
        )
        .fetchone()
    )
    if not row:
        return "Lane does not exist.", 404
    return dict(row), 200


@lane.put("/lane/<int:id>")
def update_lane(id: int):
    """Update lane."""

    form = request.form.copy().to_dict()
    form["id"] = id
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            """
            UPDATE lane SET
                updated_at = CURRENT_TIMESTAMP,
                title = :title,
                slug = :slug
            WHERE id = :id
            """,
            form,
        )
        db.commit()
    except db.ProgrammingError:
        return "Missing parameter(s).", 400
    except db.IntegrityError:
        return "Invalid parameter(s).", 400
    return "Lane successfully updated.", 201


@lane.delete("/lane/<int:id>")
def delete_lane(id: int):
    """Delete lane."""

    db = get_db()
    db.execute("DELETE FROM lane WHERE id = ?", (id,))
    db.commit()
    return "Lane successfully deleted.", 200


@lane.get("/lane")
def list_lanes():
    """List lanes."""

    rows = get_db().execute("SELECT * FROM lane").fetchall()
    if not rows:
        return "Lanes do not exist.", 404
    return list(map(dict, rows)), 200
