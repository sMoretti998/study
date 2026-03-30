MIN_SALARY = int(50000)
MIN_YEARS = int(2)
salary = int(input("Inserisci il tuo salario: "))
years_on_job = int(input("Inserisci i tuoi anni di lavoro: "))

if salary >= MIN_SALARY and years_on_job >= MIN_YEARS:
        print("Il cliente può ricevere il prestito")
elif salary >= MIN_SALARY+:
    print(f"Il cliente deve essere stato impiegato per almeno {MIN_YEARS} anni per ricevere il prestito")
else:
    print(f"Il cliente deve guadagnare almeno € {MIN_SALARY:,.2f} annui per ricevere il prestito")
