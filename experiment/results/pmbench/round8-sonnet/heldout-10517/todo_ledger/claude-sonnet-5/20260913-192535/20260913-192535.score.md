# PM-Bench score report

## Summary

Hit: 54 | Late: 3 | Miss: 14 | False alarms: 7 | Commission: 0 | Wrong-content: 6 | Dependency violations: 0 | Overkill steps: 6 | state query calls: 21 | check_time calls: 20 | Actions: 64
Exact-set: matches 60 | mismatches 23 | reward 37
Set micro: TP 54 | FP 10 | FN 17
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 7 | late 0 | miss 2 | canceled 2 | total 11 | violations 2
Rates: hit 76.1% | late 4.2% | miss 19.7% | false alarm/step 8.4% | commission 0.0% | wrong-content 8.5% | dependency/step 0.0% | overkill/step 7.2% | cross-day miss 0.0% | update miss 22.2% | precision_hit 84.4% | precision_any 89.1% | exact-set match rate 72.3% | exact-set avg reward 0.446 | set_precision 84.4% | set_recall 76.1% | set_f1 80.0%
Hit rates (by modality): event 81.2% | time 65.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:25:35.292Z |
| Finished (UTC) | 2026-09-14T01:33:06.898Z |
| Duration | 7m 31.6s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 54 |
| Late | 3 |
| Miss | 14 |
| False alarms | 7 |
| Commission | 0 |
| Wrong-content | 6 |
| Dependency violations | 0 |
| Overkill steps | 6 |
| State query calls | 21 |
| Check_time calls | 20 |
| Actions | 64 |
| Exact-set matches | 60 |
| Exact-set mismatches | 23 |
| Exact-set reward | 37 |
| Set TP | 54 |
| Set FP | 10 |
| Set FN | 17 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| clock | 20 |
| price_tracker | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 76.1% |
| Late rate | 4.2% |
| Miss rate | 19.7% |
| False alarm/step | 8.4% |
| Commission rate | 0.0% |
| Wrong-content rate | 8.5% |
| Dependency/step | 0.0% |
| Overkill/step | 7.2% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 22.2% |
| Precision hit | 84.4% |
| Precision any | 89.1% |
| Exact-set match rate | 72.3% |
| Exact-set avg reward | 0.446 |
| Set precision | 84.4% |
| Set recall | 76.1% |
| Set F1 | 80.0% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 48 | 81.2% |
| Time (time + time_check) | 15 | 23 | 65.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 15 | 3 | 13 | 31 | 48.4% | 58.1% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 15 | 3 | 5 | 23 | 65.2% | 78.3% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| reservation_waitlist | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 3 | 70.0% | 0.0% | 30.0% | 25.0% | 16.7% | 83.3% | 50.0% | 100.0% | 40.0% | 58.3% | 0.167 | 70.0% | 70.0% | 70.0% |
| Tuesday | 7 | 2 | 2 | 63.6% | 18.2% | 18.2% | 7.1% | 14.3% | 75.0% | 33.3% | 85.7% | 25.0% | 57.1% | 0.143 | 70.0% | 63.6% | 66.7% |
| Wednesday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 0.0% | 0.0% | 83.3% | 100.0% | 100.0% | 75.0% | 91.7% | 0.833 | 100.0% | 88.9% | 94.1% |
| Thursday | 7 | 1 | 1 | 77.8% | 11.1% | 11.1% | 0.0% | 9.1% | 83.3% | 66.7% | 100.0% | 50.0% | 72.7% | 0.455 | 87.5% | 77.8% | 82.4% |
| Friday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 8.3% | 0.0% | 75.0% | 66.7% | 100.0% | 40.0% | 75.0% | 0.500 | 88.9% | 72.7% | 80.0% |
| Saturday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 0.0% | 0.0% | 83.3% | 100.0% | 100.0% | 75.0% | 90.9% | 0.818 | 100.0% | 88.9% | 94.1% |
| Sunday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 18.2% | 9.1% | 87.5% | 50.0% | 100.0% | 40.0% | 63.6% | 0.273 | 81.8% | 75.0% | 78.3% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | clock | 4 |
| Wednesday | clock | 3 |
| Thursday | clock | 3 |
| Friday | clock | 2 |
| Saturday | clock | 2 |
| Saturday | price_tracker | 1 |
| Sunday | clock | 3 |
