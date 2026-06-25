from app.pipeline import CortexVisionPipeline

pipeline = CortexVisionPipeline()

world = pipeline.run()

print(world)