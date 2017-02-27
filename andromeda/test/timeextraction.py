

from andromeda.core.featureextraction import TimeExtractor


te = TimeExtractor()


print te.process('yesterday morning', time_format_str='%A, %B %d, %Y - %H:%M:%S')
