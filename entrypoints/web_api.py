from fastapi import FastAPI, HTTPException, Query
from ssn_generation.core.usecases.pesel_generator import generate_unique_ssn
from ssn_generation.dataproviders.faker_ssn_provider import generate_ssn_with_faker
from ssn_generation.core.entities.pesel import Pesel
from datetime import date, datetime

app = FastAPI(
    title="Polish SSN (PESEL) Generator and Validator",
    description="An API to generate and validate Polish PESEL numbers.",
    version="1.0.0",
)

@app.post("/generate/", tags=["PESEL Generation"])
def generate_pesels(
    num: int = Query(10, gt=0, le=10000, description="Number of PESELs to generate."),
    method: str = Query("unique", enum=["unique", "faker"], description="Generation method."),
    sex: str | None = Query(None, enum=["M", "F"], description="Sex (M/F). Required for 'unique' method."),
    start_date: date | None = Query(None, description="Start date for birth date (YYYY-MM-DD). Required for 'unique' method."),
    end_date: date | None = Query(None, description="End date for birth date (YYYY-MM-DD). Required for 'unique' method.")
):
    if method == "unique":
        if not all([sex, start_date, end_date]):
            raise HTTPException(status_code=400, detail="sex, start_date, and end_date are required for the 'unique' method.")
        try:
            pesels = generate_unique_ssn(num, sex, start_date, end_date)
            return {"pesels": pesels}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif method == "faker":
        pesels = generate_ssn_with_faker(num)
        return {"pesels": pesels}

@app.get("/validate/", tags=["PESEL Validation"])
def validate_pesel(
    pesel: str,
    sex: str | None = Query(None, enum=["M", "F"]),
    birth_date: str | None = Query(None, description="Birth date (YYYY-MM-DD)")
):
    try:
        birth_date_obj: date | None = datetime.strptime(birth_date, '%Y-%m-%d').date() if birth_date else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    p = Pesel(pesel)
    is_valid = p.is_valid(sex=sex, birth_date=birth_date_obj)

    return {"pesel": pesel, "is_valid": is_valid} 