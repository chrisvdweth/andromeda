from andromeda.core.featureextraction import LifeProcessor

print "[LifeProcessor] Start test"


lp = LifeProcessor()

print "[LifeProcessor] Process string..."
#print lp.process('In a word this hotel is magnificent.')
print lp.process('In a word this hotel is magnificent. The staff from the ground up to management were welcoming, warm and friendly.')

print "[LifeProcessor] Test finished"
