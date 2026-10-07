"""Data quality rules for the ride-hail trip records.

One rule per entry. Each `fails` predicate is SQL that is TRUE for a row that fails the rule,
so running it returns the problem rows. Dimensions follow the DAMA-DMBOK.

`meaning` records what a failure actually is once we have looked at it:
  defect             the data is wrong and should be fixed at the source
  business rule      the data is right; the rule did not know how the business works
  documentation gap  the data and the rule disagree because no spec says what should happen
  undecided          not reviewed yet
"""

DIMENSIONS = ["Completeness", "Validity", "Accuracy", "Consistency", "Timeliness", "Uniqueness"]

RULES = [
    # Completeness
    dict(id="CMP-01", dimension="Completeness", severity="medium",
         name="Pickup and dropoff zone known",
         test="Every trip has a real pickup and dropoff zone, not 'Unknown' (zones 264 and 265).",
         why="Trips in an unknown zone vanish from every map and every zone ranking, so wait times and volume by area are understated.",
         fails="PULocationID in (264, 265) or DOLocationID in (264, 265)",
         meaning="defect: TLC uses zones 264 and 265 for 'Unknown' and 'Outside of NYC'. These trips cannot be placed, so zone rankings show how many are missing."),
    dict(id="CMP-02", dimension="Completeness", severity="medium",
         name="Driver arrival time recorded",
         test="Every trip records when the driver arrived at the pickup.",
         why="Without the arrival time we cannot tell how long the rider stood waiting for the car.",
         fails="on_scene_datetime is null",
         meaning="not reviewed yet"),
    dict(id="CMP-03", dimension="Completeness", severity="low",
         name="Originating base recorded",
         test="Every trip records the base that took the original request.",
         why="Needed to trace a trip back to the business that took the booking.",
         fails="originating_base_num is null",
         meaning="documentation gap: the field is blank on 99.6% of Lyft (HV0005) trips and never on Uber. No published rule says Lyft must fill it, so it does not count against the operating numbers."),

    # Validity
    dict(id="VAL-01", dimension="Validity", severity="high",
         name="Fare is not negative",
         test="The rider's base fare is zero or more.",
         why="A negative fare pulls revenue down and breaks the driver pay share.",
         fails="base_passenger_fare < 0",
         meaning="not reviewed yet"),
    dict(id="VAL-02", dimension="Validity", severity="high",
         name="Driver pay is not negative",
         test="Driver pay is zero or more.",
         why="A driver cannot be paid less than nothing for a trip; this distorts pay figures.",
         fails="driver_pay < 0",
         meaning="not reviewed yet"),
    dict(id="VAL-03", dimension="Validity", severity="high",
         name="Dropoff comes after pickup",
         test="The dropoff time is later than the pickup time.",
         why="A trip that ends before it starts has no usable duration or speed.",
         fails="dropoff_datetime <= pickup_datetime",
         meaning="not reviewed yet"),
    dict(id="VAL-04", dimension="Validity", severity="high",
         name="Zones exist in the zone list",
         test="Pickup and dropoff zone numbers are in TLC's official zone list.",
         why="A zone number that is not on the list cannot be named or mapped.",
         fails="PULocationID not in (select LocationID from zones) or DOLocationID not in (select LocationID from zones)",
         meaning="not reviewed yet"),

    # Accuracy
    dict(id="ACC-01", dimension="Accuracy", severity="medium",
         name="Speed is believable",
         test="Average speed over the trip is 80 mph or less.",
         why="Faster than that in New York means the miles or the times are wrong.",
         fails="trip_time > 0 and trip_miles / (trip_time / 3600.0) > 80",
         meaning="not reviewed yet"),
    dict(id="ACC-02", dimension="Accuracy", severity="low",
         name="Trip is under 100 miles",
         test="A trip covers fewer than 100 miles.",
         why="Very long trips are rare; a handful of bad ones inflate miles and fares.",
         fails="trip_miles > 100",
         meaning="not reviewed yet"),
    dict(id="ACC-03", dimension="Accuracy", severity="medium",
         name="No big fares for zero-mile trips",
         test="A trip under a tenth of a mile does not charge more than $50.",
         why="A large fare with no distance is a billing or meter error.",
         fails="trip_miles < 0.1 and base_passenger_fare > 50",
         meaning="not reviewed yet"),
    dict(id="ACC-04", dimension="Accuracy", severity="medium",
         name="Driver pay is not above what the rider paid",
         test="Driver pay is no more than fare plus tips plus tolls (with a $1 allowance).",
         why="If pay often exceeds what riders paid, either the fields are wrong or the company subsidises trips; the COO needs to know which.",
         fails="driver_pay > base_passenger_fare + tips + tolls + 1",
         meaning="business rule: mostly Uber. Companies top up driver pay on cheap or discounted trips, so this is how the business works. Still shown beside driver pay share."),

    # Consistency
    dict(id="CON-01", dimension="Consistency", severity="medium",
         name="Trip time matches the clock",
         test="The recorded trip time is within a minute of dropoff minus pickup.",
         why="Two ways of measuring the same trip should agree; when they do not, duration and speed are unreliable.",
         fails="abs(trip_time - date_diff('second', pickup_datetime, dropoff_datetime)) > 60",
         meaning="not reviewed yet"),
    dict(id="CON-02", dimension="Consistency", severity="high",
         name="Request comes before pickup",
         test="The ride is requested before the rider is picked up.",
         why="This is the start of every wait time; if it is out of order the wait is negative.",
         fails="request_datetime > pickup_datetime",
         meaning="defect: times out of order. These trips are left out of every wait time figure."),
    dict(id="CON-03", dimension="Consistency", severity="medium",
         name="Driver arrives after the request",
         test="The driver arrives at the pickup after the ride was requested.",
         why="Arriving before the request makes the driver's travel time to the rider negative.",
         fails="on_scene_datetime < request_datetime",
         meaning="defect: times out of order. These trips are left out of every wait time figure."),
    dict(id="CON-04", dimension="Consistency", severity="medium",
         name="Driver arrives before pickup",
         test="The driver arrives at the pickup no later than the pickup time.",
         why="A rider cannot be picked up before the car is there.",
         fails="on_scene_datetime > pickup_datetime",
         meaning="not reviewed yet"),

    # Timeliness
    dict(id="TML-01", dimension="Timeliness", severity="medium",
         name="Trip is filed in its own month",
         test="Each trip sits in the monthly file for the month it was picked up.",
         why="Misfiled trips land in the wrong month's totals and are late for the month they belong to.",
         fails="strftime(pickup_datetime, '%Y-%m') <> file_month",
         meaning="not reviewed yet"),

    # Uniqueness
    dict(id="UNQ-01", dimension="Uniqueness", severity="medium",
         name="No duplicate trips",
         test="No trip appears more than once (same company, times, zones, miles, fare and pay).",
         why="Duplicates double count trips and revenue.",
         fails="dup_count > 1",
         meaning="not reviewed yet"),
]
