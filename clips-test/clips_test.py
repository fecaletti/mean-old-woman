import clips

env = clips.Environment()

rule = """
(defrule my-rule
  (my-fact first-slot)
  =>
  (printout t "My Rule fired!" crlf))
"""
env.build(rule)

for rule in env.rules():
    print(rule)

print("Done!")