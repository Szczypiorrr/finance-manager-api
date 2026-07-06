from sqlalchemy.orm import Session
from app.services.user import get_user_by_id
from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate
from app.helpers.validators import validate_amount
from app.exceptions.goal_exceptions import GoalNotFound, GoalAlreadyExists, GoalTargetAmountExceeded

def get_goals(db: Session, user_id: int = None, limit: int = 10, offset: int = 0):
    query = db.query(Goal)

    if user_id is not None:
        query = query.where(Goal.user_id == user_id)

    return query.limit(limit).offset(offset).all()

def get_goal_by_id(goal_id: int, db: Session):
    goal = db.query(Goal).where(Goal.id == goal_id).first()

    if not goal:
        raise GoalNotFound()
    
    return goal

def get_goal_by_name(name: str, db: Session):
    return db.query(Goal).where(Goal.name == name).first()

def create_goal(goal: GoalCreate, db: Session):
    get_user_by_id(user_id=goal.user_id, db=db)

    validate_amount(goal.target_amount)

    if get_goal_by_name(name=goal.name, db=db):
        raise GoalAlreadyExists()

    goal_db = Goal(
        target_amount = goal.target_amount,
        current_amount = 0,
        name = goal.name,
        user_id = goal.user_id
    )

    db.add(goal_db)
    db.commit()
    db.refresh(goal_db)

    return goal_db

def delete_goal(goal_id: int, db: Session):
    goal = get_goal_by_id(goal_id=goal_id, db=db)

    db.delete(goal)
    db.commit()

    return

def update_goal(goal_id: int, goal_update: GoalUpdate, db: Session):
    goal = get_goal_by_id(goal_id=goal_id, db=db)

    if goal_update.name is not None:
        existing_goal = get_goal_by_name(name=goal_update.name, db=db)

        if existing_goal and existing_goal.id != goal.id:
            raise GoalAlreadyExists()

        goal.name = goal_update.name

    if goal_update.target_amount is not None:
        validate_amount(goal_update.target_amount)
        goal.target_amount = goal_update.target_amount


    db.commit()
    db.refresh(goal)

    return goal

def deposit_to_goal(goal_id: int, user_id: int, amount: int, db: Session):
    goal = get_goal_by_id(goal_id=goal_id, db=db)

    if goal.user_id != user_id:
        raise GoalNotFound()

    validate_amount(amount)

    if goal.current_amount + amount > goal.target_amount:
        raise GoalTargetAmountExceeded()

    goal.current_amount += amount

    db.commit()
    db.refresh(goal)

    return goal