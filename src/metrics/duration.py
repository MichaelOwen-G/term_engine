
from enum import Enum

class DurationMetrics(Enum):
    '''
    Defines the metrics or Units for the time duration
    '''
    MICROSECONDS = 1
    MILLISECONDS = 2
    SECONDS = 3
    MINUTES = 4
    HOURS = 5


class Duration:
    def __init__(self, metrics: DurationMetrics, duration: int):
        '''
        Holds the duration of a time

        - Args:
        - metrics (DurationMetrics): The metrics of the duration
        - duration (int): The duration of the time
        '''
        # validate arguments
        # metrics should be of type DurationMetrics
        if not isinstance(metrics, DurationMetrics):
            raise TypeError("metrics must be of type DurationMetrics")
        
        # duration should be of type int
        if not isinstance(duration, int):
            raise TypeError("duration must be of type int")
        
        # set properties
        self._metrics: DurationMetrics = metrics
        self._duration: int = duration

    ''' GETTERS $ SETTERS '''
    @property
    def metrics(self):
        return self._metrics
    
    @metrics.setter
    def metrics(self, metrics):
        pass

    @property
    def duration(self):
        return self._duration
    
    @duration.setter
    def duration(self, duration):
        pass

    @property
    def microSeconds(self):
        return self._duration_in_metric(DurationMetrics.MICROSECONDS)
    
    @microSeconds.setter
    def microSeconds(self, duration):
        pass

    @property
    def milliSeconds(self):
        return self._duration_in_metric(DurationMetrics.MILLISECONDS)
            
            
    @milliSeconds.setter
    def milliSeconds(self, duration):
        pass

    @property
    def seconds(self):
        return self._duration_in_metric(DurationMetrics.SECONDS)
            
    @seconds.setter
    def seconds(self, duration):
        pass

    @property
    def minutes(self):
       return self._duration_in_metric(DurationMetrics.MINUTES)
    
    @minutes.setter
    def minutes(self, duration):
        pass

    def _duration_in_metric(self, metric: 'DurationMetrics') -> int:
        '''
        '''
        # validate arguments
        # metric should be of type DurationMetrics
        if not isinstance(metric, DurationMetrics):
            raise TypeError("other must be of type DurationMetrics")

        # if the metrics are the same, return the duration
        if (self._metrics == metric):
            return self._duration
        
        # convert self.metric to the other metric
        
        # create a switch statement for
        # all the DuratiomMetrics options
        match self._metrics:
            case DurationMetrics.MICROSECONDS:
                return self._microSeconds_to(metric)       
            case DurationMetrics.MILLISECONDS:
                return self._milliSeconds_to(metric)
            case DurationMetrics.SECONDS:
                return self._seconds_to(metric)
            case DurationMetrics.MINUTES:
                return self._minutes_to(metric)
            case DurationMetrics.HOURS:
                return self._hours_to(metric)
                    
        
    '''
     TIME CONVERSIONS
    '''

    ''' FOR MILLISECONDS'''
    def _milliSeconds_to(self, other: DurationMetrics) -> int:
        match other:
            case DurationMetrics.MICROSECONDS:
                return self._duration * 1000
            case DurationMetrics.SECONDS:
                return self._duration / 1000
            case DurationMetrics.MINUTES:
                return self._duration / 60000
            case DurationMetrics.HOURS:
                return self._duration / 3600000

    ''' FOR MICROSECONDS'''    
    def _microSeconds_to(self, other: DurationMetrics) -> int:
        match other:
            case DurationMetrics.MICROSECONDS:
                return self._duration
            case DurationMetrics.SECONDS:
                return self._duration / 1000000
            case DurationMetrics.MINUTES:
                return self._duration / 60000000
            case DurationMetrics.HOURS:
                return self._duration / 3600000000
            
    ''' FOR SECONDS'''
    def _seconds_to(self, other: DurationMetrics) -> int:
        match other:
            case DurationMetrics.MICROSECONDS:
                return self._duration * 1000000
            case DurationMetrics.MILLISECONDS:
                return self._duration * 1000
            case DurationMetrics.MINUTES:
                return self._duration / 60
            case DurationMetrics.HOURS:
                return self._duration / 3600
    
    ''' FOR MINUTES'''
    def _minutes_to(self, other: DurationMetrics) -> int:
        match other:
            case DurationMetrics.MICROSECONDS:
                return self._duration * 60000000
            case DurationMetrics.MILLISECONDS:
                return self._duration * 60000
            case DurationMetrics.SECONDS:
                return self._duration * 60
            case DurationMetrics.HOURS:
                return self._duration / 60
    
    ''' FOR HOURS'''
    def _hours_to(self, other: DurationMetrics) -> int:
        match other:
            case DurationMetrics.MICROSECONDS:
                return self._duration * 3600000000
            case DurationMetrics.MILLISECONDS:
                return self._duration * 3600000
            case DurationMetrics.SECONDS:
                return self._duration * 3600
            case DurationMetrics.MINUTES:
                return self._duration * 60
        

    ''''
    MATH OPERTAIONS
    '''
    def _validateOtherForMath(self, other: 'Duration') -> None:
        '''
        - Validates the other duration for math operations
        - Raises an error if other is not of type Duration
        - Raises an error if the metrics are not the same
        '''
        # validate arguments
        # other should be of type Duration
        if not isinstance(other, Duration):
            raise TypeError("other must be of type Duration")
        
        # metrics should be the same
        if self._metrics != other._metrics:
            raise ValueError("Cannot do math operations on durations with different metrics")

    def add_duration(self, duration: int, other_metric: DurationMetrics) -> None:
        '''
        Add the duration: int to the current duration
        Args:
            - duration: int
            - other: DurationMetrics
        '''
        # convert the current duration to the argument other_metric
        # then add the duration to be added
        newDur: int = self._duration_in_metric(other_metric) + duration

        self._duration = newDur

    def add(self, other: 'Duration') -> 'Duration':
        '''
        Adds two durations together
        - Can only be done if the metrics are the same
        '''
        # validate if math operations can be done on Other 
        self._validateOtherForMath(other)
        
        # add the durations
        self._duration += other.duration

        return self

    def subtract(self, other: 'Duration') -> 'Duration':
        '''
        Subtracts two durations
        - Can only be done if the metrics are the same
        '''

        # validate if math operations can be done on Other 
        self._validateOtherForMath(other)
        
        # subtract the durations
        newDur: int = self._duration - other._duration

        self._duration = newDur if newDur > 0 else 0

        return self
    
    def __eq__(self, other: 'Duration') -> bool:
        return self._metrics == other.metrics and self._duration == other.duration