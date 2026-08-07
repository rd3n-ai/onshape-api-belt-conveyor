# Parametric Belt Conveyor

A belt conveyor — frame, end rollers, belt, legs, load — generated entirely
from code with [build123d](https://github.com/gumyr/build123d). No manual
CAD editing: change a parameter, re-run, get a new valid assembly.

```bash
pip install -r requirements.txt
python conveyor.py
```

This produces `conveyor.step` (native CAD exchange) and `conveyor.stl`
(preview it right here on GitHub — click the file above).

## Parameters

| Name | Meaning | Default |
|---|---|---|
| `CONVEYOR_LENGTH` | Overall length | 1000 mm |
| `CONVEYOR_WIDTH` | Belt width | 300 mm |
| `ROLLER_DIAMETER` | End drum diameter | 60 mm |
| `FRAME_HEIGHT` | Side frame height | 80 mm |
| `FRAME_THICKNESS` | Side frame wall thickness | 5 mm |
| `LEG_HEIGHT` | Support leg height | 400 mm |

## Same approach, taken further

This script is the minimal, runnable core of a modeling pattern I use in
production: the same parametric logic, driven through the [Onshape
REST API](https://onshape-public.github.io/docs/) instead of a local library,
scales to a fully toleranced 82-part assembly — bearings, motor mount, chain
guard, welded frame, belt loop — built and positioned entirely by script,
zero manual clicking in the CAD GUI.

I design and quote real conveyor systems for manufacturers this way. If
you're evaluating AI-assisted mechanical design work, this repo is the
"show me the code" version of that process.

## Background

I'm a mechanical design engineer (SolidWorks, 11 years, 100+ projects) who
builds AI-assisted CAD tooling for my own consulting work.
<!-- TODO(Nizam): add your LinkedIn/website URL here before publishing -->


## License

MIT — use it, fork it, build on it.
