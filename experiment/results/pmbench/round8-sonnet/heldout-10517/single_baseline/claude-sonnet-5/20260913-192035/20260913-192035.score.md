# PM-Bench score report

## Summary

Hit: 56 | Late: 1 | Miss: 14 | False alarms: 3 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 3 | state query calls: 29 | check_time calls: 27 | Actions: 60
Exact-set: matches 66 | mismatches 17 | reward 49
Set micro: TP 56 | FP 4 | FN 15
Cross-day: hit 6 | late 0 | miss 1 | total 7
Updates: hit 6 | late 0 | miss 3 | canceled 2 | total 11 | violations 1
Rates: hit 78.9% | late 1.4% | miss 19.7% | false alarm/step 3.6% | commission 0.0% | wrong-content 4.2% | dependency/step 0.0% | overkill/step 3.6% | cross-day miss 14.3% | update miss 33.3% | precision_hit 93.3% | precision_any 95.0% | exact-set match rate 79.5% | exact-set avg reward 0.590 | set_precision 93.3% | set_recall 78.9% | set_f1 85.5%
Hit rates (by modality): event 81.2% | time 73.9%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-09-14T01:20:35.933Z |
| Finished (UTC) | 2026-09-14T01:26:24.042Z |
| Duration | 5m 48.1s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 56 |
| Late | 1 |
| Miss | 14 |
| False alarms | 3 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 3 |
| State query calls | 29 |
| Check_time calls | 27 |
| Actions | 60 |
| Exact-set matches | 66 |
| Exact-set mismatches | 17 |
| Exact-set reward | 49 |
| Set TP | 56 |
| Set FP | 4 |
| Set FN | 15 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 1 |
| clock | 27 |
| price_tracker | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 78.9% |
| Late rate | 1.4% |
| Miss rate | 19.7% |
| False alarm/step | 3.6% |
| Commission rate | 0.0% |
| Wrong-content rate | 4.2% |
| Dependency/step | 0.0% |
| Overkill/step | 3.6% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 33.3% |
| Precision hit | 93.3% |
| Precision any | 95.0% |
| Exact-set match rate | 79.5% |
| Exact-set avg reward | 0.590 |
| Set precision | 93.3% |
| Set recall | 78.9% |
| Set F1 | 85.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 48 | 81.2% |
| Time (time + time_check) | 17 | 23 | 73.9% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 1 | 40 | 97.5% | 97.5% |
| proactive_monitoring_required | 17 | 1 | 13 | 31 | 54.8% | 58.1% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| clock | 17 | 1 | 5 | 23 | 73.9% | 78.3% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| laundry_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| price_tracker | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| reservation_waitlist | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 3 | 70.0% | 0.0% | 30.0% | 0.0% | 0.0% | 83.3% | 50.0% | 100.0% | 40.0% | 75.0% | 0.500 | 100.0% | 70.0% | 82.4% |
| Tuesday | 9 | 1 | 1 | 81.8% | 9.1% | 9.1% | 0.0% | 7.1% | 87.5% | 66.7% | 100.0% | 50.0% | 78.6% | 0.571 | 90.0% | 81.8% | 85.7% |
| Wednesday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 0.0% | 0.0% | 66.7% | 100.0% | 80.0% | 75.0% | 91.7% | 0.833 | 100.0% | 77.8% | 87.5% |
| Thursday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 0.0% | 0.0% | 83.3% | 100.0% | 100.0% | 75.0% | 90.9% | 0.818 | 100.0% | 88.9% | 94.1% |
| Friday | 8 | 0 | 3 | 72.7% | 0.0% | 27.3% | 8.3% | 0.0% | 75.0% | 66.7% | 100.0% | 40.0% | 75.0% | 0.500 | 88.9% | 72.7% | 80.0% |
| Saturday | 8 | 0 | 1 | 88.9% | 0.0% | 11.1% | 0.0% | 0.0% | 83.3% | 100.0% | 100.0% | 75.0% | 90.9% | 0.818 | 100.0% | 88.9% | 94.1% |
| Sunday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 18.2% | 18.2% | 87.5% | 50.0% | 100.0% | 40.0% | 54.5% | 0.091 | 81.8% | 75.0% | 78.3% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 4 |
| Tuesday | bank_balance | 1 |
| Tuesday | clock | 5 |
| Wednesday | clock | 4 |
| Thursday | clock | 5 |
| Friday | clock | 3 |
| Saturday | clock | 3 |
| Saturday | price_tracker | 1 |
| Sunday | clock | 3 |
