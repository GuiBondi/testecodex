"""Validation utilities for CPF and phone numbers."""
import re


def validate_cpf(cpf: str) -> bool:
    """Validate a Brazilian CPF using the mod 11 algorithm."""
    if not cpf.isdigit() or len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False

    def calc_digit(digs: str) -> str:
        s = sum(int(d) * w for d, w in zip(digs, range(len(digs) + 1, 1, -1)))
        r = 11 - s % 11
        return "0" if r >= 10 else str(r)

    dig1 = calc_digit(cpf[:9])
    dig2 = calc_digit(cpf[:9] + dig1)
    return cpf[-2:] == dig1 + dig2


def validate_phone(telefone: str) -> bool:
    """Validate Brazilian phone numbers with 10-13 digits."""
    digits = re.sub(r"\D", "", telefone)
    return digits.isdigit() and 10 <= len(digits) <= 13
