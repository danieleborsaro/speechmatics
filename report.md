# Report: Speechmatics programming task V2

## Original script version

The original version of the script to be fixed suffers from a number if issues, the main ones being:

1. RESTful API is called without a valid schema: the subsequent exception is not captured and the execution fails
2. It refers a non-existent property of the returned JSON data (worng capitalisation)
3. The main logic is flawed in two ways:
   1. It calls the API once every second, for a minute, instead of once every minute for an hour (and the loop ranges over the wrong interval)
   2. It records timestamps for the same turnaround the wrong way, and only the first one is actually returned to the user
4. It returns GMT times as returned by the API instead of EST as requested
5. Unorthodox coding style differing from official guidelines (eg: imported modules that are not used, same module imported multiple times, wrong indentation, non rigorous return of composite values in functions, ...)

## Fixes

1. Correct URI for RESTful API call, by specifying the protocol to be used
2. Fix reference to 'Average_Turnaround_Mins'
3. Correct range of main loop: we want to check Speechmatics service status every minute for an hour. The semantic uderlined by this requirement can be unclear, therefore we decide that we check the status:
   1. right at the beginning of the script execution;
   2. once every minute;
   3. once at the beginning of the next hour, in order to cover the entire hour and avoid leaving out the last minute.
   In total, we want to call the API 62 times, meaning the loop must range on: 0, 61
4. Correct sleeping time of '60', instead of '1'
5. Fix how samples are recorded. Considering that we are interested in only the maximum turnaround, there is no point (inefficient) in recording all samples
   1. we maintain only one 'max_turnaround' variable, storing the maximum value for turnaround so far returned
   2. the list of times now will contain timestamps for the maximum turnaround only.
   A change in logic is required so that:
   1. Both variables are reinitialised upon reception of a new maximum turnaround value (and special attention must be paid for the initial value):
      * 'max_turnaround' gets the new maximum
      * times gets the timestamp associated to the new maxmum
   2. Receptions of the same maxmimum means we need to add their timestamps to the list of times. Here requirements are not entirely clear: we need to return times of when the maxmimum turnaround was 'measured', and we decide that this must refer to the measurement happened on Speechmatics side (as opposed to measured by the client/script). This means we need to add timestamps than are not already recorded.
6. We implement the missing timezone conversion of timestamps from GMT (as returned by the API) to EST (as requested). Instead of cluttering the main() with timeconversion instruction, a dedicated function is provided to hide specific logic.

## Enhancements

A number of enhancements can be implemented to benefit the code quality in terms of readability and maintainability. I actually consider them to be an integral part of proper software development and think that the time necessary to implemen them is misleadingly considerend time wasted and better overlooked during rushed coding stints.

1. Fix coding style (a linter is helpful in highliting the targetted style)
2. Comments should be always provided as preambles to modules and functions and for prompt clarification of specific business logic (not so much about the 'how', but to the 'why' code was written the way it is)
3. No explicit constants should be used anywhere. Define constants instead and refer to them

## E-mail to the customer

Dear Mr.X,

in regards yur request for a Speechmatics service status turnaround statistics, we are now able to provide you with an updated version that fixes the issues you raised with us last time. You can  dowload it from our support portal by logging in with your credentials.

I would like to further apologise for having provided you with an unstable version of the tool and for the delay you had to endure: although not formally released, the tool ended up splipping through the validation stages of our release process. We made sure this was not the case with this lastes version we are providing you this time. In fact, we identified why we failed to validate the orginal verions and took appropriate actions in order to enhance our development process and prevent similar situations from occurring again.

The tool is now satisfying the original requirements and is now ready for UAT on your part. Please let us know about new issues or should you want to refine some of its functionalities before going ahead with the formal release steps.

Regards,

Daniele Borsaro

