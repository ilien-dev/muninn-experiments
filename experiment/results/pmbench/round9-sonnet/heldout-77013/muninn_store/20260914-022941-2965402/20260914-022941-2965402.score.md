# PM-Bench score report

## Summary

Hit: 64 | Late: 0 | Miss: 17 | False alarms: 3 | Commission: 0 | Wrong-content: 1 | Dependency violations: 0 | Overkill steps: 3 | state query calls: 744 | check_time calls: 84 | Actions: 67
Exact-set: matches 64 | mismatches 20 | reward 44
Set micro: TP 64 | FP 3 | FN 17
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 9 | late 0 | miss 0 | canceled 2 | total 11 | violations 0
Rates: hit 79.0% | late 0.0% | miss 21.0% | false alarm/step 3.6% | commission 0.0% | wrong-content 1.2% | dependency/step 0.0% | overkill/step 3.6% | cross-day miss 0.0% | update miss 0.0% | precision_hit 95.5% | precision_any 95.5% | exact-set match rate 76.2% | exact-set avg reward 0.524 | set_precision 95.5% | set_recall 79.0% | set_f1 86.5%
Hit rates (by modality): event 69.6% | time 100.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T08:29:41.932Z |
| Finished (UTC) | 2026-09-14T08:37:55.543Z |
| Duration | 8m 13.6s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 64 |
| Late | 0 |
| Miss | 17 |
| False alarms | 3 |
| Commission | 0 |
| Wrong-content | 1 |
| Dependency violations | 0 |
| Overkill steps | 3 |
| State query calls | 744 |
| Check_time calls | 84 |
| Actions | 67 |
| Exact-set matches | 64 |
| Exact-set mismatches | 20 |
| Exact-set reward | 44 |
| Set TP | 64 |
| Set FP | 3 |
| Set FN | 17 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 66 |
| bank_balance | 66 |
| calendar | 66 |
| clock | 84 |
| course_portal | 66 |
| email | 66 |
| laundry_status | 66 |
| library_hold | 66 |
| price_tracker | 66 |
| reservation_waitlist | 66 |
| shipment_status | 66 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 79.0% |
| Late rate | 0.0% |
| Miss rate | 21.0% |
| False alarm/step | 3.6% |
| Commission rate | 0.0% |
| Wrong-content rate | 1.2% |
| Dependency/step | 0.0% |
| Overkill/step | 3.6% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 0.0% |
| Precision hit | 95.5% |
| Precision any | 95.5% |
| Exact-set match rate | 76.2% |
| Exact-set avg reward | 0.524 |
| Set precision | 95.5% |
| Set recall | 79.0% |
| Set F1 | 86.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 56 | 69.6% |
| Time (time + time_check) | 25 | 25 | 100.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 24 | 0 | 16 | 40 | 60.0% | 60.0% |
| proactive_monitoring_required | 40 | 0 | 1 | 41 | 97.6% | 97.6% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 2 | 0 | 0 | 2 | 100.0% | 100.0% |
| bank_balance | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| calendar | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| clock | 25 | 0 | 0 | 25 | 100.0% | 100.0% |
| course_portal | 2 | 0 | 0 | 2 | 100.0% | 100.0% |
| email | 2 | 0 | 0 | 2 | 100.0% | 100.0% |
| laundry_status | 2 | 0 | 0 | 2 | 100.0% | 100.0% |
| library_hold | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| price_tracker | 3 | 0 | 1 | 4 | 75.0% | 75.0% |
| shipment_status | 1 | 0 | 0 | 1 | 100.0% | 100.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 0 | 3 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 40.0% | 100.0% | 25.0% | 100.0% | 76.9% | 0.538 | 100.0% | 66.7% | 80.0% |
| Tuesday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 0.0% | 0.0% | 75.0% | 100.0% | 66.7% | 100.0% | 81.8% | 0.636 | 100.0% | 83.3% | 90.9% |
| Wednesday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 0.0% | 0.0% | 60.0% | 100.0% | 50.0% | 100.0% | 85.7% | 0.714 | 100.0% | 77.8% | 87.5% |
| Thursday | 14 | 0 | 2 | 87.5% | 0.0% | 12.5% | 0.0% | 0.0% | 84.6% | 100.0% | 80.0% | 100.0% | 80.0% | 0.600 | 100.0% | 87.5% | 93.3% |
| Friday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 16.7% | 16.7% | 62.5% | 100.0% | 40.0% | 100.0% | 58.3% | 0.167 | 80.0% | 72.7% | 76.2% |
| Saturday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 62.5% | 100.0% | 60.0% | 85.7% | 75.0% | 0.500 | 100.0% | 75.0% | 85.7% |
| Sunday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 8.3% | 8.3% | 77.8% | 100.0% | 66.7% | 100.0% | 75.0% | 0.500 | 90.9% | 83.3% | 87.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 9 |
| Monday | bank_balance | 9 |
| Monday | calendar | 9 |
| Monday | clock | 13 |
| Monday | course_portal | 9 |
| Monday | email | 9 |
| Monday | laundry_status | 9 |
| Monday | library_hold | 9 |
| Monday | price_tracker | 9 |
| Monday | reservation_waitlist | 9 |
| Monday | shipment_status | 9 |
| Tuesday | appointment_portal | 8 |
| Tuesday | bank_balance | 8 |
| Tuesday | calendar | 8 |
| Tuesday | clock | 11 |
| Tuesday | course_portal | 8 |
| Tuesday | email | 8 |
| Tuesday | laundry_status | 8 |
| Tuesday | library_hold | 8 |
| Tuesday | price_tracker | 8 |
| Tuesday | reservation_waitlist | 8 |
| Tuesday | shipment_status | 8 |
| Wednesday | appointment_portal | 9 |
| Wednesday | bank_balance | 9 |
| Wednesday | calendar | 9 |
| Wednesday | clock | 14 |
| Wednesday | course_portal | 9 |
| Wednesday | email | 9 |
| Wednesday | laundry_status | 9 |
| Wednesday | library_hold | 9 |
| Wednesday | price_tracker | 9 |
| Wednesday | reservation_waitlist | 9 |
| Wednesday | shipment_status | 9 |
| Thursday | appointment_portal | 9 |
| Thursday | bank_balance | 9 |
| Thursday | calendar | 9 |
| Thursday | clock | 10 |
| Thursday | course_portal | 9 |
| Thursday | email | 9 |
| Thursday | laundry_status | 9 |
| Thursday | library_hold | 9 |
| Thursday | price_tracker | 9 |
| Thursday | reservation_waitlist | 9 |
| Thursday | shipment_status | 9 |
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
| Saturday | appointment_portal | 12 |
| Saturday | bank_balance | 12 |
| Saturday | calendar | 12 |
| Saturday | clock | 12 |
| Saturday | course_portal | 12 |
| Saturday | email | 12 |
| Saturday | laundry_status | 12 |
| Saturday | library_hold | 12 |
| Saturday | price_tracker | 12 |
| Saturday | reservation_waitlist | 12 |
| Saturday | shipment_status | 12 |
| Sunday | appointment_portal | 9 |
| Sunday | bank_balance | 9 |
| Sunday | calendar | 9 |
| Sunday | clock | 12 |
| Sunday | course_portal | 9 |
| Sunday | email | 9 |
| Sunday | laundry_status | 9 |
| Sunday | library_hold | 9 |
| Sunday | price_tracker | 9 |
| Sunday | reservation_waitlist | 9 |
| Sunday | shipment_status | 9 |
