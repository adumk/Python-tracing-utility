My Python tracing utility that measures the execution time of specific functions in a python program is implemented in 'Profiler.py' file. I used my previous project to test and develop it in practice, that's why there are many other files.
The utility is implemented without modifying the target functions directly - there is only one call at the beginning of "main.py". This also ensures minimal overhead when tracing is disabled.
The relevant files are:
1. Profiler.py
2. main.py - the profiler is called at the beginning. 


Follow these steps to set up and run the project locally.
In PyCharm:
1. Clone or download the project from this github repository.
2. Open project in PyCharm and install required packages.
3. Run 'main.py' file. You should see a console with logs:
   
   Profiler loaded. Type 'start' to enable it.


      ">>> Profiler commands [results / start / stop]:"

      The program is freezed for 10 seconds to allow user read text and then type 'start' to enable profiler. After 10 seconds program is running, if user typed 'start' then more logs will appear in console.

4. If the profiler is enabled there will be logs "Calling {function_name}" just to visualize for user what functions are called and how many times. All these calls and their durations will be analized.

5. To look at intermediate results without stopping the profiler type "results" - a table in console will appear.

6. Type "stop" to disable profiler and see results table too. In this mode called functions are not measured, program just remember the data gained so far. It's also impossible to see intermediate results.

7. To enable profiler again type "start". Utility will continue to measure functions and merge data with previous data.

   I encourage You to take under two minutes and let the program to be fully executed. As You see "Program executed." in console You can look at bigger dataset in table. You can enable and disable profiler multiple times during program         execution.
   After full execution there is a function freezing program for a long time to allow user to see gained dataset.
