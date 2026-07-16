class PasswordVerifier:
    def verify(self, password: str | None) -> bool:
        self._check_not_null(password)
        # After null check, password is guaranteed to be str
        assert password is not None  # For type checker
        self._check_length(password)
        self._check_uppercase(password)
        self._check_lowercase(password)
        self._check_has_number(password)
        return True

    def _check_not_null(self, password: str | None) -> None:
        if password is None:
            raise Exception("Password should not be null")

    def _check_length(self, password: str) -> None:
        if len(password) <= 8:
            raise Exception("Password should be longer than 8 characters")

    def _check_uppercase(self, password: str) -> None:
        if not any(c.isupper() for c in password):
            raise Exception("Password should have at least one uppercase letter")

    def _check_lowercase(self, password: str) -> None:
        if not any(c.islower() for c in password):
            raise Exception("Password should have at least one lowercase letter")

    def _check_has_number(self, password: str) -> None:
        if not any(c.isdigit() for c in password):
            raise Exception("Password should have at least one number")
