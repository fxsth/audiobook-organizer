import tagger
import splitter
import ntpath
from metadata import Audiobookmeta

dir = "/home/felix/Cornelia Funke/Cornelia Funke - Tintenherz"
searchterm = ntpath.basename(dir)

audiobookmeta = Audiobookmeta("Cornelia Funke - Tintenherz")
result = audiobookmeta.tryRetrieveFromITunes()
# print(result)
outputDir = dir+"/Tintenherz"
splitter.create_dir(outputDir)
# splitter.splitIfNecessary(dir, outputDir, "Tintenherz")
# splitter.renameAllAfterSplitting(outputDir, "Tintenherz")
tagger.tagAllInDirectory(outputDir, audiobookmeta)