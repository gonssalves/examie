from flask_login import current_user
from flask import flash, redirect, url_for

def admin_login_required():
    def decorator(view_func):
        from functools import wraps
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated and str(current_user.role) == 'Admin':
                return view_func(*args, **kwargs)
            else:
                # Handle unauthorized access
                # You can redirect to a login page or return an error response
                # For example:
                flash("You don't have permission to access this page")
                return redirect(url_for('main.index'))
                return "Unauthorizedd", 401
        return wrapper
    return decorator

def admin_teacher_login_required():
    def decorator(view_func):
        from functools import wraps
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            from flask_login import current_user
            if current_user.is_authenticated and str(current_user.role) == 'Admin' or str(current_user.role) == 'Teacher':
                return view_func(*args, **kwargs)
            else:
                # Handle unauthorized access
                # You can redirect to a login page or return an error response
                # For example:
                flash("You don't have permission to access this page")
                return redirect(url_for('main.index'))
                return "Unauthorizedd", 401
        return wrapper
    return decorator