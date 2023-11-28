import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlalchemy

from gandai.db import connect_with_connector

db = connect_with_connector()


def weekly_cumulative_events(event_type="validate") -> pd.DataFrame:
    statement = """
    SELECT 
        e.*, 
        to_timestamp(e.created) as dt,  
        EXTRACT(DOW FROM TO_TIMESTAMP(e.created)) as dow,
        a.name, 
        s.label,
        COUNT(*) OVER (PARTITION BY e.actor_key ORDER BY date_trunc('minute', to_timestamp(e.created))) as cumulative_events
    FROM event e
    JOIN actor a on e.actor_key = a.key
    JOIN search s on e.search_uid = s.uid
    WHERE 
        to_timestamp(e.created) >= date_trunc('week', current_date)
        AND a.key not in ('grata','dealcloud','7138248581')
        AND e.type = :event_type
    ORDER BY e.actor_key, date_trunc('minute', to_timestamp(e.created))
    """
    with db.connect() as conn:
        result = conn.execute(sqlalchemy.text(statement), {"event_type": event_type})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


def draw_weekly_cumulative(event_type: str) -> px.line:
    df = weekly_cumulative_events(event_type=event_type)
    return px.line(
        df,
        x="dt",
        y="cumulative_events",
        color="name",
        title=f"{event_type}",
    )


def draw_validation_per_day() -> pd.DataFrame:
    statement = """
    SELECT e.*, to_timestamp(e.created) as dt, a.name, s.label
    FROM event e
    JOIN actor a on e.actor_key = a.key
    JOIN search s on e.search_uid = s.uid
    WHERE to_timestamp(e.created) > now() - interval '14 day'
    and a.key not in ('grata','dealcloud')
    and e.type in ('validate')
    ORDER BY created
    """
    with db.connect() as conn:
        result = conn.execute(sqlalchemy.text(statement))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    df["date"] = df["dt"].dt.strftime("%Y-%m-%d")

    validations = (
        df.groupby(["name", "date", "label"])
        .size()
        .reset_index(name="count")
        .sort_values(by=["date"])
        .reset_index(drop=True)
    )

    fig = px.bar(
        validations,
        x="date",
        y="count",
        color="name",
        barmode="group",
        title="Validations per day by search by researcher | Trailing 7 days",
        hover_data=["label"],
    )
    return fig


def draw_leaderboard(window: str = "month", title: str = "") -> go.Figure:
    # window = 'month'
    statement = f"""
        SELECT 
            a.name,
            e.type,
            count(DISTINCT e.domain) as count
        FROM event e
        JOIN actor a on e.actor_key = a.key
        WHERE 
            to_timestamp(e.created) >= date_trunc('{window}', current_date)
            AND e.type in ('validate','reject','send','client_approve','client_conflict','client_reject')
            AND a.type = 'research'
        GROUP BY a.name, e.type
        """
    with db.connect() as conn:
        result = conn.execute(sqlalchemy.text(statement))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    pivot_df = (
        df.pivot(index="name", columns="type", values="count").fillna(0).reset_index()
    )
    pivot_df = pivot_df[
        [
            "name",
            "validate",
            "reject",
            "send",
            "client_approve",
            "client_conflict",
            "client_reject",
        ]
    ]
    pivot_df = pivot_df.sort_values(by="validate", ascending=False).reset_index(
        drop=True
    )
    pivot_df["numerator"] = pivot_df["client_approve"] + pivot_df["client_conflict"]
    pivot_df["denominator"] = (
        pivot_df["client_approve"]
        + pivot_df["client_conflict"]
        + pivot_df["client_reject"]
    )
    totals = pivot_df.sum(numeric_only=True)
    totals["name"] = "Total"  # Add a total label in the 'name' column
    totals_df = pd.DataFrame([totals], columns=pivot_df.columns)
    display_df = pd.concat([pivot_df, totals_df], ignore_index=True)
    display_df["approval_rating"] = round(
        display_df["numerator"] / display_df["denominator"], 2
    ).fillna(0)
    display_df

    ## render table
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=list(display_df.columns), align="left"),
                cells=dict(
                    values=[
                        display_df[col] for col in display_df.columns
                    ],  # Use display_df to include the totals
                    align="left",
                ),
            )
        ]
    )

    fig.update_layout(title_text=title, title_font=dict(size=24))
    return fig
