from ref_fields import REF_FIELDS

class Citation:
    def __init__(self, ref_info: list):
        self.id = ref_info[0]
        self.ref_info = ref_info[1:]

    def get_field(self, field_name: str):
        if field_name == 'id':
            return self.id
        if field_name in REF_FIELDS:
            return self.ref_info[REF_FIELDS.index(field_name)]
        raise ValueError(f"Field '{field_name}' is not a valid reference field.")

    def __str__(self):
        return f"Citation({', '.join(f'{field}={getattr(self, field)}' for field in REF_FIELDS)})"
