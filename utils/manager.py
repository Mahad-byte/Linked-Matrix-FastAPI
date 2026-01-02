import functools
from fastapi import HTTPException, status
from models.users import User, Profile


def manager_required(func):

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Extract current_user from kwargs
        current_user: User = kwargs.get("current_user")

        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )

        # Get the user's profile to check role
        profile = await Profile.find_one(Profile.user_id == current_user.id)

        if not profile or profile.role.value != "PM":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Project Managers (PM) can access this resource",
            )

        return await func(*args, **kwargs)

    return wrapper
