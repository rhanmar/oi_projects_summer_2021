from .auth_views import (
    UserLoginView,
    UserPasswordResetConfirmView,
    UserPasswordResetView,
    UserRegisterView,
)
from .report import UserAddReportView
from .reviews import (
    UserAddReviewView,
    UserDeleteReviewView,
    UserDetailReviewView,
    UserEditReviewView,
    UserReviewsView,
)
from .user_profile_views import (
    BannedUserView,
    UserAddToBlacklistView,
    UserBlacklistView,
    UserEditProfileView,
    UserProfileView,
    UserRemoveFromBlacklistView,
)
from .welcome_page import IndexView
