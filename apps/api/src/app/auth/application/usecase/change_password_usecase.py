
class ChangePasswordUseCase:
    def __init__(self, user_repository, password_service):
        self.user_repository = user_repository
        self.password_service = password_service

    def execute(self, user_id, old_password, new_password):
        # Fetch the user from the repository
        user = self.user_repository.get_user_by_id(user_id)
        
        # Check if the old password is correct
        if not self.password_service.verify_password(old_password, user.password_hash):
            raise ValueError("Old password is incorrect")
        
        # Hash the new password
        new_password_hash = self.password_service.hash_password(new_password)
        
        # Update the user's password in the repository
        user.password_hash = new_password_hash
        self.user_repository.update_user(user)
        
        return True