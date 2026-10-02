# PM-Bench score report

## Summary

Hit: 56 | Late: 0 | Miss: 15 | False alarms: 4 | Commission: 0 | Wrong-content: 2 | Dependency violations: 0 | Overkill steps: 4 | state query calls: 613 | check_time calls: 83 | Actions: 60
Exact-set: matches 64 | mismatches 19 | reward 45
Set micro: TP 56 | FP 4 | FN 15
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 8 | late 0 | miss 1 | canceled 2 | total 11 | violations 0
Rates: hit 78.9% | late 0.0% | miss 21.1% | false alarm/step 4.8% | commission 0.0% | wrong-content 2.8% | dependency/step 0.0% | overkill/step 4.8% | cross-day miss 0.0% | update miss 11.1% | precision_hit 93.3% | precision_any 93.3% | exact-set match rate 77.1% | exact-set avg reward 0.542 | set_precision 93.3% | set_recall 78.9% | set_f1 85.5%
Hit rates (by modality): event 68.8% | time 100.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:26:25.565Z |
| Finished (UTC) | 2026-09-14T01:34:46.002Z |
| Duration | 8m 20.4s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 56 |
| Late | 0 |
| Miss | 15 |
| False alarms | 4 |
| Commission | 0 |
| Wrong-content | 2 |
| Dependency violations | 0 |
| Overkill steps | 4 |
| State query calls | 613 |
| Check_time calls | 83 |
| Actions | 60 |
| Exact-set matches | 64 |
| Exact-set mismatches | 19 |
| Exact-set reward | 45 |
| Set TP | 56 |
| Set FP | 4 |
| Set FN | 15 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 53 |
| bank_balance | 53 |
| calendar | 53 |
| clock | 83 |
| course_portal | 53 |
| email | 53 |
| laundry_status | 53 |
| library_hold | 53 |
| price_tracker | 53 |
| reservation_waitlist | 53 |
| shipment_status | 53 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 78.9% |
| Late rate | 0.0% |
| Miss rate | 21.1% |
| False alarm/step | 4.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 2.8% |
| Dependency/step | 0.0% |
| Overkill/step | 4.8% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 11.1% |
| Precision hit | 93.3% |
| Precision any | 93.3% |
| Exact-set match rate | 77.1% |
| Exact-set avg reward | 0.542 |
| Set precision | 93.3% |
| Set recall | 78.9% |
| Set F1 | 85.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 33 | 48 | 68.8% |
| Time (time + time_check) | 23 | 23 | 100.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 25 | 0 | 15 | 40 | 62.5% | 62.5% |
| proactive_monitoring_required | 31 | 0 | 0 | 31 | 100.0% | 100.0% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| bank_balance | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| clock | 23 | 0 | 0 | 23 | 100.0% | 100.0% |
| email | 2 | 0 | 0 | 2 | 100.0% | 100.0% |
| laundry_status | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| price_tracker | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| reservation_waitlist | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| shipment_status | 1 | 0 | 0 | 1 | 100.0% | 100.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 2 | 80.0% | 0.0% | 20.0% | 8.3% | 8.3% | 66.7% | 100.0% | 60.0% | 100.0% | 75.0% | 0.500 | 88.9% | 80.0% | 84.2% |
| Tuesday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 7.1% | 7.1% | 62.5% | 100.0% | 57.1% | 100.0% | 71.4% | 0.429 | 88.9% | 72.7% | 80.0% |
| Wednesday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 0.0% | 0.0% | 66.7% | 100.0% | 60.0% | 100.0% | 83.3% | 0.667 | 100.0% | 77.8% | 87.5% |
| Thursday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 9.1% | 9.1% | 66.7% | 100.0% | 60.0% | 100.0% | 72.7% | 0.455 | 87.5% | 77.8% | 82.4% |
| Friday | 9 | 0 | 2 | 81.8% | 0.0% | 18.2% | 8.3% | 8.3% | 75.0% | 100.0% | 66.7% | 100.0% | 75.0% | 0.500 | 90.0% | 81.8% | 85.7% |
| Saturday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 0.0% | 0.0% | 66.7% | 100.0% | 60.0% | 100.0% | 81.8% | 0.636 | 100.0% | 77.8% | 87.5% |
| Sunday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 0.0% | 0.0% | 75.0% | 100.0% | 71.4% | 100.0% | 81.8% | 0.636 | 100.0% | 83.3% | 90.9% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 4 |
| Monday | bank_balance | 4 |
| Monday | calendar | 4 |
| Monday | clock | 12 |
| Monday | course_portal | 4 |
| Monday | email | 4 |
| Monday | laundry_status | 4 |
| Monday | library_hold | 4 |
| Monday | price_tracker | 4 |
| Monday | reservation_waitlist | 4 |
| Monday | shipment_status | 4 |
| Tuesday | appointment_portal | 14 |
| Tuesday | bank_balance | 14 |
| Tuesday | calendar | 14 |
| Tuesday | clock | 14 |
| Tuesday | course_portal | 14 |
| Tuesday | email | 14 |
| Tuesday | laundry_status | 14 |
| Tuesday | library_hold | 14 |
| Tuesday | price_tracker | 14 |
| Tuesday | reservation_waitlist | 14 |
| Tuesday | shipment_status | 14 |
| Wednesday | appointment_portal | 6 |
| Wednesday | bank_balance | 6 |
| Wednesday | calendar | 6 |
| Wednesday | clock | 12 |
| Wednesday | course_portal | 6 |
| Wednesday | email | 6 |
| Wednesday | laundry_status | 6 |
| Wednesday | library_hold | 6 |
| Wednesday | price_tracker | 6 |
| Wednesday | reservation_waitlist | 6 |
| Wednesday | shipment_status | 6 |
| Thursday | appointment_portal | 4 |
| Thursday | bank_balance | 4 |
| Thursday | calendar | 4 |
| Thursday | clock | 11 |
| Thursday | course_portal | 4 |
| Thursday | email | 4 |
| Thursday | laundry_status | 4 |
| Thursday | library_hold | 4 |
| Thursday | price_tracker | 4 |
| Thursday | reservation_waitlist | 4 |
| Thursday | shipment_status | 4 |
| Friday | appointment_portal | 10 |
| Friday | bank_balance | 10 |
| Friday | calendar | 10 |
| Friday | clock | 12 |
| Friday | course_portal | 10 |
| Friday | email | 10 |
| Friday | laundry_status | 10 |
| Friday | library_hold | 10 |
| Friday | price_tracker | 10 |
| Friday | reservation_waitlist | 10 |
| Friday | shipment_status | 10 |
| Saturday | appointment_portal | 8 |
| Saturday | bank_balance | 8 |
| Saturday | calendar | 8 |
| Saturday | clock | 11 |
| Saturday | course_portal | 8 |
| Saturday | email | 8 |
| Saturday | laundry_status | 8 |
| Saturday | library_hold | 8 |
| Saturday | price_tracker | 8 |
| Saturday | reservation_waitlist | 8 |
| Saturday | shipment_status | 8 |
| Sunday | appointment_portal | 7 |
| Sunday | bank_balance | 7 |
| Sunday | calendar | 7 |
| Sunday | clock | 11 |
| Sunday | course_portal | 7 |
| Sunday | email | 7 |
| Sunday | laundry_status | 7 |
| Sunday | library_hold | 7 |
| Sunday | price_tracker | 7 |
| Sunday | reservation_waitlist | 7 |
| Sunday | shipment_status | 7 |
