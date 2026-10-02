# PM-Bench score report

## Summary

Hit: 57 | Late: 3 | Miss: 21 | False alarms: 5 | Commission: 0 | Wrong-content: 4 | Dependency violations: 0 | Overkill steps: 6 | state query calls: 33 | check_time calls: 29 | Actions: 65
Exact-set: matches 53 | mismatches 27 | reward 26
Set micro: TP 57 | FP 8 | FN 24
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 6 | late 1 | miss 2 | canceled 2 | total 11 | violations 2
Rates: hit 70.4% | late 3.7% | miss 25.9% | false alarm/step 6.2% | commission 0.0% | wrong-content 4.9% | dependency/step 0.0% | overkill/step 7.5% | cross-day miss 0.0% | update miss 22.2% | precision_hit 87.7% | precision_any 92.3% | exact-set match rate 66.2% | exact-set avg reward 0.325 | set_precision 87.7% | set_recall 70.4% | set_f1 78.1%
Hit rates (by modality): event 70.2% | time 70.8%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:01:25.120Z |
| Finished (UTC) | 2026-09-14T01:09:29.343Z |
| Duration | 8m 4.2s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 57 |
| Late | 3 |
| Miss | 21 |
| False alarms | 5 |
| Commission | 0 |
| Wrong-content | 4 |
| Dependency violations | 0 |
| Overkill steps | 6 |
| State query calls | 33 |
| Check_time calls | 29 |
| Actions | 65 |
| Exact-set matches | 53 |
| Exact-set mismatches | 27 |
| Exact-set reward | 26 |
| Set TP | 57 |
| Set FP | 8 |
| Set FN | 24 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 2 |
| clock | 29 |
| email | 1 |
| library_hold | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 70.4% |
| Late rate | 3.7% |
| Miss rate | 25.9% |
| False alarm/step | 6.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 4.9% |
| Dependency/step | 0.0% |
| Overkill/step | 7.5% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 22.2% |
| Precision hit | 87.7% |
| Precision any | 92.3% |
| Exact-set match rate | 66.2% |
| Exact-set avg reward | 0.325 |
| Set precision | 87.7% |
| Set recall | 70.4% |
| Set F1 | 78.1% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 40 | 57 | 70.2% |
| Time (time + time_check) | 17 | 24 | 70.8% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 40 | 0 | 2 | 42 | 95.2% | 95.2% |
| proactive_monitoring_required | 17 | 3 | 19 | 39 | 43.6% | 51.3% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 17 | 2 | 5 | 24 | 70.8% | 79.2% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 55.6% | 100.0% | 83.3% | 50.0% | 76.9% | 0.538 | 100.0% | 66.7% | 80.0% |
| Tuesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 7.7% | 7.7% | 57.1% | 75.0% | 100.0% | 42.9% | 61.5% | 0.231 | 87.5% | 63.6% | 73.7% |
| Wednesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 20.0% | 10.0% | 66.7% | 0.0% | 100.0% | 0.0% | 50.0% | 0.000 | 75.0% | 54.5% | 63.2% |
| Thursday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 0.0% | 9.1% | 88.9% | 33.3% | 100.0% | 25.0% | 72.7% | 0.455 | 90.0% | 75.0% | 81.8% |
| Friday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 83.3% | 0.667 | 90.9% | 83.3% | 87.0% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 10.0% | 10.0% | 80.0% | 75.0% | 100.0% | 50.0% | 60.0% | 0.200 | 91.7% | 78.6% | 84.6% |
| Sunday | 6 | 1 | 2 | 66.7% | 11.1% | 22.2% | 9.1% | 18.2% | 60.0% | 75.0% | 75.0% | 60.0% | 54.5% | 0.091 | 75.0% | 66.7% | 70.6% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | clock | 5 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 2 |
| Thursday | clock | 4 |
| Friday | clock | 6 |
| Friday | email | 1 |
| Friday | library_hold | 1 |
| Saturday | clock | 4 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 5 |
