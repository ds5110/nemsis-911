from pathlib import Path
import pandas as pd


def main():
    """Map important variables to categorical variables and give them meaningful names."""
    fp = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'events.pickle'
    df = pd.read_pickle(fp)

    # The field "eArrest_18" is "End of EMS Cardiac Arrest Event". Map to a categorical variable.
    dead, alive, ongoing, unknown = "Dead", "Alive", "Ongoing", "Unknown"
    map_e_arrest_18 = {
        3018001: dead,     # Expired in ED
        3018003: dead,     # Expired in the Field
        3018005: ongoing,  # Ongoing Resuscitation in ED
        3018007: alive,    # ROSC in the Field
        3018009: alive,    # ROSC in the ED
        3018011: ongoing   # Ongoing Resuscitation by Other EMS
    }
    df['eArrest_18'] = df['eArrest_18'].map(arg=map_e_arrest_18).fillna(unknown).astype("category")
    df.rename(columns={"eArrest_18": "End_of_EMS_Cardiac_Arrest_Event"}, inplace=True)

    # The field "eOutcome_01" is "Emergency Department Disposition". Map to a categorical variable.
    def map_e_outcome_01(code: int) -> str:
        if code == 20:
            return dead
        elif pd.isna(code):
            return unknown
        else:
            return alive
    df['eOutcome_01'] = df['eOutcome_01'] \
        .map(arg=lambda code: map_e_outcome_01(code), na_action='ignore') \
        .fillna(unknown) \
        .astype("category")

    # The field "eArrest_05" is "CPR Care Provided Prior to EMS Arrival". Map to a categorical variable.
    map_e_arrest_05 = {
        9923001: "No",
        9923003: "Yes"
    }
    df['eArrest_05'] = df['eArrest_05'] \
        .map(arg=map_e_arrest_05, na_action='ignore') \
        .fillna(unknown) \
        .astype("category")
    df.rename(columns={"eArrest_05": "CPR_Care_Provided_Prior_to_EMS_Arrival"}, inplace=True)

    # Save as a new pickle file.
    save_path = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'events_renamed.pickle'
    df.to_pickle(path=save_path)


if __name__ == "__main__":
    main()
