# 82-Part Belt Conveyor — Designed Entirely Through the Onshape API

**Live design (view in browser, no account needed):**
https://cad.onshape.com/documents/054f879de5e8a01d53c7d133/w/7df0627cb16755143864b0bb/e/f5fc55eb78c4656677873cb6

This is a real conveyor I use as a reference when quoting jobs for manufacturers —
not a toy demo. Every sketch, extrude, and part placement in it was created by
issuing REST API calls to Onshape, driven by plain-language instructions in
[Claude Code](https://claude.com/claude-code). No manual clicking in the CAD GUI.

## The design

- **Frame:** welded 40×80 steel profile
- **Envelope:** 500 mm belt width × 2500 mm length × 850 mm height
- **Rollers:** Ø100 mm drums
- **Hardware:** UCF pillow-block bearings + bolts, standard content inserted by
  cross-document assembly reference
- **Drive:** motor mount + chain guard
- **Belt:** modeled as a closed loop around both drums
- **82 parts**, fully resolved assembly with a generated BOM

## How the Claude Code + Onshape system works

The loop I actually use, on this model and on client jobs:

1. **I describe engineering intent in plain language** — dimensions, tolerances,
   which standard hardware to use, how sub-assemblies should relate to each other.
2. **Claude Code turns that into Onshape REST API calls** — sketch features,
   extrudes, transforms — hitting the same endpoints the Onshape web app itself
   uses (`/partstudios/.../features`, `/assemblies/.../instances`, etc.).
3. **Every step is verified before the next one starts** — `GET /parts` to confirm
   the part count changed as expected, bounding-box checks, rendered shaded views —
   so errors get caught immediately instead of compounding.
4. **I review the result like any other CAD output** — geometry, tolerances,
   whether it actually matches what I'd hand-model. If it's wrong, we fix the
   API call, not the part.

This isn't "AI designs the machine" — it's the same design decisions I'd make by
hand, executed through a scriptable interface instead of mouse clicks, which is
what makes iteration on parametric families fast.

## What we actually ran into

The honest version, not the highlight reel — these are the real obstacles solved
along the way:

- **Extrude offsets are silently ignored by the API.** No error, the feature just
  doesn't offset. Fix: extrude on a default plane, then move the part into place
  with a `transform` feature using its deterministic part ID.
- **Sketching directly on a face created by a previous feature throws an error.**
  Staying on the three default planes and positioning everything with transforms
  afterward sidesteps this entirely.
- **A sketch region with a hole fills in both regions on extrude** — the outer
  profile and the hole both become solid. Fix: split the profile into separate,
  non-overlapping sketches per region instead of one sketch with a nested contour.
- **Arcs need explicit start/end parameters in radians**, not just two endpoints —
  found by comparing what the GUI generates against what the API expects.
- **Inserting standard content (bearings, bolts) across documents** required
  placing one example by hand once, then reading back the assembly's JSON to see
  the exact API call it produced — the pattern isn't documented up front.

None of this is exotic — it's the normal process of learning an API by probing
it, the same as any other integration work. The difference is that the "user"
issuing the calls and reading the responses is Claude Code, working from my
engineering spec instead of me writing the HTTP requests by hand.

## What the calls actually look like

A sketch + extrude feature is a `POST` with a feature-definition JSON body —
no different in shape from any other REST API:

```
POST /api/v10/partstudios/d/{did}/w/{wid}/e/{eid}/features
{
  "feature": {
    "btType": "BTMFeature-134",
    "featureType": "extrude",
    "parameters": [
      { "btType": "BTMParameterEnum-145", "parameterId": "endBound", "value": "BLIND" },
      { "btType": "BTMParameterQuantity-147", "parameterId": "depth", "expression": "5 mm" },
      { "btType": "BTMParameterQueryList-148", "parameterId": "entities", "queries": [ /* sketch region */ ] }
    ]
  }
}
```

Every feature call is followed by a read-back to confirm it did what was
intended before moving on:

```
GET /api/v10/partstudios/d/{did}/w/{wid}/e/{eid}/parts
```

Compare the returned part count/IDs against what should have changed. If it
doesn't match, the previous call gets fixed before anything is built on top of it.

## About

Mechanical design engineer (SolidWorks, 11 years, 100+ projects).

## License

MIT — this documentation and the process description are free to reuse. The
linked Onshape document is mine; fork it in Onshape if you want to build on
the actual model.
