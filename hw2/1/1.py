import numpy
import json

m = numpy.load("first_task.npy")
md = numpy.diag(m)
sd = numpy.diag(numpy.fliplr(m))
stats = {"sum": int(m.sum()), "mean": float(m.mean()), "sumMD": int(md.sum()), "avrMD": float(md.mean()), "sumSD": int(sd.sum()),
          "avrSD": float(sd.mean()), "max": int(m.max()), "min": int(m.min())}
with open("first_task_result.json", "w") as outfile:
    json.dump(stats, outfile, indent=4)

numpy.save("first_task_result.npy", m / m.sum())