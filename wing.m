%
% Cessna 172 CFD data from here:
% https://www.researchgate.net/publication/353752543_Cessna_172_Flight_Simulation_Data
%

% Pasted from the PDF
clean_orig = [
-180.0 -0.1778 0.0338 -0.2003
-170.0 0.4214 0.1030 0.1698
-160.0 0.7273 0.2816 0.3023
-150.0 0.9408 0.5539 0.6037
-130.0 1.2311 1.0571 0.6426
-120.0 1.3786 1.3222 0.5786
-110.0 1.4243 1.5438 0.3609
-100.0 1.4615 1.7340 0.1532
-90.0 1.4643 1.8145 -0.0913
-80.0 1.4349 1.8377 -0.3946
-70.0 1.3377 1.7304 -0.6656
-60.0 1.0434 1.5605 -0.8998
-50.0 0.9365 1.2568 -0.9829
-40.0 0.7292 0.9692 -1.0146
-30.0 0.5856 0.6722 -0.9432
-25.0 0.4891 0.5140 -0.8370
-20.0 0.3465 0.3618 -0.7529
-17.0 0.5161 0.3047 -0.7588
-14.0 0.4126 0.2144 -0.7404
-12.0 0.2684 0.1722 -0.8554
-10.0 0.1682 0.1034 -0.7501
-9.0 0.1571 0.0906 -0.6842
-8.0 0.1421 0.0783 -0.6075
-7.0 0.1347 0.0651 -0.5321
-6.0 0.1199 0.0568 -0.4424
-5.0 0.1090 0.0489 -0.3557
-4.0 0.0992 0.0418 -0.2679
-3.0 0.0830 0.0372 -0.1789
-2.0 0.0691 0.0336 -0.0889
-1.0 0.0513 0.0314 0.0049
0.0 0.0315 0.0306 0.0998
1.0 0.0126 0.0311 0.1944
2.0 -0.0026 0.0329 0.2898
3.0 -0.0282 0.0349 0.3881
4.0 -0.0551 0.0398 0.4839
5.0 -0.0741 0.0449 0.5799
6.0 -0.0982 0.0521 0.6679
7.0 -0.1174 0.0607 0.7532
8.0 -0.1509 0.0694 0.8487
9.0 -0.1773 0.0807 0.9357
10.0 -0.2064 0.0925 1.0151
11.0 -0.2390 0.1063 1.0895
12.0 -0.2639 0.1206 1.1607
13.0 -0.2971 0.1369 1.2240
14.0 -0.3254 0.1525 1.2558
15.0 -0.3631 0.1726 1.2930
17.0 -0.5042 0.2169 1.1411
20.0 -0.5533 0.3184 1.1328
25.0 -0.6826 0.4824 1.0309
40.0 -0.7076 0.9254 1.0062
50.0 -0.9984 1.2527 1.0285
60.0 -1.0141 1.4544 0.8901
70.0 -1.3370 1.8579 0.7527
80.0 -1.4293 1.9547 0.5114
90.0 -1.5130 1.9055 0.1421
100.0 -1.5670 1.8449 -0.1712
110.0 -1.5886 1.6785 -0.4155
120.0 -1.5085 1.4831 -0.5821
130.0 -1.3977 1.2191 -0.6926
140.0 -1.2469 0.8872 -0.7399
150.0 -1.1508 0.7052 -0.9188
160.0 -0.8942 0.3447 -0.5876
170.0 -0.8425 0.1365 -0.7211
180.0 -0.1756 0.0339 -0.1950]

tailoff = [
-180.0 0.0298 -0.1710 -0.0570
-170.0 0.0967 0.0630 0.2040
-160.0 0.2776 0.3320 0.3080
-140.0 0.6842 0.5100 0.4580
-130.0 0.8782 0.5090 0.4850
-120.0 1.0930 0.4170 0.4880
-110.0 1.2410 0.2640 0.4620
-100.0 1.4079 0.1010 0.4480
-90.0 1.4391 -0.0870 0.4240
-80.0 1.4722 -0.3260 0.3560
-70.0 1.3311 -0.5330 0.2440
-60.0 1.2737 -0.7370 0.2170
-50.0 1.0418 -0.8160 0.1610
-40.0 0.7928 -0.8270 0.0740
-30.0 0.5500 -0.7710 0.0110
-25.0 0.4280 -0.6900 -0.0030
-20.0 0.3060 -0.6330 -0.0240
-17.0 0.2303 -0.5750 -0.0560
-14.0 0.1721 -0.6010 -0.0690
-12.0 0.1383 -0.7340 -0.0840
-10.0 0.0835 -0.6390 -0.1170
-9.0 0.0718 -0.5840 -0.1090
-8.0 0.0631 -0.5170 -0.0990
-7.0 0.0520 -0.4450 -0.0920
-6.0 0.0452 -0.3640 -0.0860
-5.0 0.0391 -0.2830 -0.0790
-4.0 0.0341 -0.2000 -0.0750
-3.0 0.0299 -0.1190 -0.0680
-2.0 0.0274 -0.0360 -0.0630
-1.0 0.0260 0.0500 -0.0600
0.0 0.0268 0.1370 -0.0580
1.0 0.0267 0.2240 -0.0550
2.0 0.0291 0.3130 -0.0550
3.0 0.0319 0.4010 -0.0550
4.0 0.0366 0.4850 -0.0560
5.0 0.0417 0.5760 -0.0580
6.0 0.0486 0.6540 -0.0590
7.0 0.0562 0.7350 -0.0620
8.0 0.0644 0.8200 -0.0660
9.0 0.0740 0.8980 -0.0700
10.0 0.0851 0.9680 -0.0740
11.0 0.0969 1.0320 -0.0760
12.0 0.1097 1.0960 -0.0820
13.0 0.1235 1.1500 -0.0840
14.0 0.1368 1.1660 -0.0790
15.0 0.1545 1.1960 -0.0850
17.0 0.1863 0.9820 -0.0570
20.0 0.2641 0.9600 -0.0650
25.0 0.3856 0.8130 -0.0610
40.0 0.7971 0.8380 -0.1300
50.0 1.0567 0.8370 -0.2130
60.0 1.2355 0.7410 -0.2630
70.0 1.5629 0.6210 -0.3740
80.0 1.6306 0.4160 -0.4100
90.0 1.6088 0.0850 -0.5150
100.0 1.5656 -0.1780 -0.6040
110.0 1.4494 -0.3640 -0.6300
120.0 1.2192 -0.5000 -0.6320
130.0 1.0382 -0.6320 -0.6440
140.0 0.7815 -0.6770 -0.6090
150.0 0.5442 -0.6570 -0.5460
160.0 0.2884 -0.5130 -0.4510
170.0 0.0986 -0.4690 -0.3780
180.0 0.0299 -0.1720 -0.0570]

flap30 = [
-180.0 0.0529 -0.3225 -0.0537
-170.0 0.1285 -0.0078 0.1557
-160.0 0.2538 0.0817 0.2389
-150.0 0.4664 0.3472 0.3547
-140.0 0.6771 0.4230 0.4251
-130.0 0.8993 0.4518 0.4534
-120.0 1.1161 0.3756 0.4537
-110.0 1.2438 0.2542 0.4307
-100.0 1.2982 0.0757 0.4046
-90.0 1.3878 -0.1005 0.3600
-80.0 1.3816 -0.3092 0.2814
-70.0 1.2298 -0.4511 0.2076
-60.0 1.1352 -0.6089 0.1662
-50.0 0.9081 -0.6506 0.0561
-40.0 0.6980 -0.6471 0.0009
-30.0 0.4615 -0.5254 -0.0844
-25.0 0.3435 -0.4201 -0.0917
-20.0 0.2442 -0.3710 -0.1092
-17.0 0.1858 -0.3083 -0.1330
-14.0 0.1458 -0.3807 -0.1384
-12.0 0.0868 -0.2800 -0.2210
-10.0 0.0711 -0.1308 -0.2163
-9.0 0.0648 -0.0469 -0.2149
-8.0 0.0616 0.0293 -0.2075
-7.0 0.0574 0.1202 -0.2068
-6.0 0.0560 0.2120 -0.2047
-5.0 0.0560 0.2945 -0.2001
-4.0 0.0556 0.3790 -0.1971
-3.0 0.0578 0.4673 -0.1965
-2.0 0.0604 0.5478 -0.1945
-1.0 0.0643 0.6360 -0.1956
0.0 0.0692 0.7182 -0.1937
1.0 0.0750 0.8025 -0.1941
2.0 0.0817 0.8879 -0.1957
3.0 0.0888 0.9666 -0.1974
4.0 0.0974 1.0448 -0.1980
5.0 0.1064 1.1310 -0.2020
6.0 0.1161 1.1935 -0.2011
7.0 0.1270 1.2598 -0.2029
8.0 0.1382 1.3319 -0.2052
9.0 0.1495 1.3858 -0.2039
10.0 0.1612 1.4321 -0.2020
11.0 0.1731 1.4757 -0.2014
12.0 0.1837 1.4940 -0.1945
13.0 0.1926 1.4795 -0.1825
14.0 0.2490 1.2353 -0.1672
15.0 0.2482 1.2053 -0.1510
17.0 0.2834 1.0751 -0.1414
20.0 0.3758 1.1163 -0.1603
25.0 0.5225 1.0239 -0.1690
40.0 1.0254 1.0974 -0.2130
50.0 1.2443 1.0122 -0.2561
60.0 1.3797 0.8102 -0.2864
70.0 1.6451 0.6594 -0.3595
80.0 1.5071 0.2967 -0.3949
90.0 1.6190 0.0959 -0.4701
100.0 1.6395 -0.2250 -0.5878
110.0 1.3622 -0.4290 -0.5930
120.0 1.1828 -0.5559 -0.5994
130.0 0.9879 -0.6638 -0.6013
140.0 0.6681 -0.6541 -0.5477
150.0 0.4482 -0.6421 -0.4967
160.0 0.2649 -0.6563 -0.4489
170.0 0.0876 -0.7738 -0.3934
180.0 0.0529 -0.3225 -0.0537];

% Columns are not in same order for clean table as the other two, so fix that first!
clean = [clean_orig(:,1) clean_orig(:,3) clean_orig(:,4) clean_orig(:,2)]

% Note that the Flaps 30 data appears also be "tail-off"
% (ie: with the tail component removed)
% Also note that the different data sets are not sampled at the identical AoA

figure
subplot(3, 1, 1)
hold on
plot(clean(:,1), clean(:,2), 'b') # Drag
plot(clean(:,1), clean(:,3), 'r') # Lift
plot(clean(:,1), clean(:,4), 'g') # Moment
title("Clean")
grid
grid minor

subplot(3, 1, 2)
hold on
plot(tailoff(:,1), tailoff(:,2), 'b') # Drag
plot(tailoff(:,1), tailoff(:,3), 'r') # Lift
plot(tailoff(:,1), tailoff(:,4), 'g') # Moment
title("Tail-Off")
grid
grid minor

subplot(3, 1, 3)
hold on
plot(flap30(:,1), flap30(:,2), 'b') # Drag
plot(flap30(:,1), flap30(:,3), 'r') # Lift
plot(flap30(:,1), flap30(:,4), 'g') # Moment
title("Flap30")
grid
grid minor

figure
hold on
plot(clean(:,1), clean(:,3), 'b') # Lift
plot(flap30(:,1), flap30(:,3), 'r') # Lift
plot(tailoff(:,1), tailoff(:,3), 'g') # Lift
title("Lift: Clean(b), Flap30(r), Tail-off(g)")

figure
hold on
plot(clean(:,1), clean(:,2), 'b')
plot(flap30(:,1), flap30(:,2), 'r')
plot(tailoff(:,1), tailoff(:,2), 'g')
title("Drag: Clean(b), Flap30(r), Tail-off(g)")

figure
hold on
plot(clean(:,1), clean(:,4), 'b')
plot(flap30(:,1), flap30(:,4), 'r')
plot(tailoff(:,1), tailoff(:,4), 'g')
title("Moment: Clean(b), Flap30(r), Tail-off(g)")

clean_lift_resampled   = interp1(clean(:,1), clean(:,3), [-180:1:180]);
flap30_lift_resampled  = interp1(flap30(:,1), flap30(:,3), [-180:1:180]);
tailoff_lift_resampled = interp1(tailoff(:,1), tailoff(:,3), [-180:1:180]);
flap30_lift_delta  = flap30_lift_resampled - tailoff_lift_resampled;

clean_drag_resampled   = interp1(clean(:,1), clean(:,2), [-180:1:180]);
flap30_drag_resampled  = interp1(flap30(:,1), flap30(:,2), [-180:1:180]);
tailoff_drag_resampled = interp1(tailoff(:,1), tailoff(:,2), [-180:1:180]);
flap30_drag_delta  = flap30_drag_resampled - tailoff_drag_resampled;

clean_moment_resampled   = interp1(clean(:,1), clean(:,4), [-180:1:180]);
flap30_moment_resampled  = interp1(flap30(:,1), flap30(:,4), [-180:1:180]);
tailoff_moment_resampled = interp1(tailoff(:,1), tailoff(:,4), [-180:1:180]);
flap30_moment_delta  = flap30_moment_resampled - tailoff_moment_resampled;

% Max Coefficient of Lift ought to be about 1.6
% Per http://airfoiltools.com/airfoil/details?airfoil=naca2412-il
scale_factor = 1.6 / max(clean_lift_resampled);
printf("Scaling lift by %f\n", scale_factor)
clean_lift_resampled = clean_lift_resampled * scale_factor;
tailoff_lift_resampled = tailoff_lift_resampled * scale_factor;
flap30_lift_resampled = flap30_lift_resampled * scale_factor;

% Min Coefficient of Drag ought to be about 0.006
% Per http://airfoiltools.com/airfoil/details?airfoil=naca2412-il
scale_factor = 0.006 / min(clean_drag_resampled);
printf("Scaling drag by %f\n", scale_factor)
clean_drag_resampled = clean_drag_resampled * scale_factor;
tailoff_drag_resampled = tailoff_drag_resampled * scale_factor;
flap30_drag_resampled = flap30_drag_resampled * scale_factor;

figure
hold on
plot(clean_lift_resampled, 'b')
plot(clean_lift_resampled + flap30_lift_delta, 'r')
grid
grid minor
title("Resampled Lift - Clean(b), Flap30(r)")

figure
hold on
plot(clean_drag_resampled, 'b')
plot(clean_drag_resampled + flap30_drag_delta, 'r')
grid
grid minor
title("Resampled Drag - Clean(b), Flap30(r)")

figure
hold on
plot(clean_moment_resampled, 'b')
plot(clean_moment_resampled + flap30_moment_delta, 'r')
grid
grid minor
title("Resampled Moment - Clean(b), Flap30(r)")

fp = fopen("wing_tables.py", "w");
fprintf(fp, "clean_tab = [\n");
for ii = 1:361
  if ii > 1
    fprintf(fp, ",\n");
  end
  fprintf(fp, "(%.5f, %.5f, %.5f)", clean_lift_resampled(ii), clean_drag_resampled(ii), clean_moment_resampled(ii));
end
fprintf(fp, "\n]\n\n");

fprintf(fp, "flap30_delta_tab = [\n");
for ii = 1:361
  if ii > 1
    fprintf(fp, ",\n");
  end
  fprintf(fp, "(%.5f, %.5f, %.5f)", flap30_lift_delta(ii), flap30_drag_delta(ii), flap30_moment_delta(ii));
end
fprintf(fp, "\n]\n");
fclose(fp);




