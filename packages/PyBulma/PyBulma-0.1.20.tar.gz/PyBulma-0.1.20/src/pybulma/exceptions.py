class CompileError(Exception):

    def __init__(self, name):
        message = f"Compile Exception in {name}"
        super().__init__(message)


class PreTemplateError(Exception):

    def __init__(self, name, e):
        super().__init__(f"Failure in compiling pre_template in class: {name} Exception: {e}")


class PostTemplateError(Exception):

    def __init__(self, name, e):
        super().__init__(f"Failure in compiling post_template in class: {name} Exception: {e}")


class PrettifyError(Exception):

    def __init__(self, name, e):
        super().__init__(f"Failure in BS$ prettify html. Class:{name}  Exception: {e}")
