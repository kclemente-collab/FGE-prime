# Niagara Raven Moisture Binary Prototype v0.1

Status: PROTOTYPE / NOT COMPILED
Target: Raven living-obsidian moisture activation test bed

## Binary state

`MoistureBinary = 0` = dry shell

`MoistureBinary = 1` = activated wet shell

A hysteresis gate prevents visual chatter:

- activate when `PressureNormalized >= 0.62`
- remain active until `PressureNormalized <= 0.38`

## Niagara parameters

- `User.PressureNormalized` float 0..1
- `User.MoistureBinary` int 0|1
- `User.MoistureAmount` float 0..1
- `User.FilmThicknessNm` float, target range 120..780
- `User.EmissionActivation` float 0..1
- `User.DropletSpawnRate` float

## Update logic

```text
if MoistureBinary == 0 and PressureNormalized >= 0.62:
    MoistureBinary = 1

if MoistureBinary == 1 and PressureNormalized <= 0.38:
    MoistureBinary = 0

MoistureAmount = critically_damped_lerp(MoistureAmount, MoistureBinary, 0.18s)
FilmThicknessNm = lerp(120, 780, MoistureAmount)
EmissionActivation = smoothstep(0.35, 0.92, MoistureAmount)
DropletSpawnRate = MoistureBinary * 14
```

## Render expression binding

`MoistureAmount` feeds RavenMoistureShell `Moisture`.

`FilmThicknessNm` feeds RavenWavelengthResponse `thicknessNm`.

`EmissionActivation` feeds the wavelength-driven emission layer.

## Acceptance gates

1. Dry state retains living-obsidian identity.
2. Wet activation does not replace substrate with generic chrome.
3. Binary transition has no frame chatter.
4. Film response remains view-angle dependent.
5. Emission remains subordinate to shell physics.
6. Raven identity silhouette and facial landmarks are unaffected.

## Validation status

Source logic drafted. Niagara graph, UE compile, GPU simulation, and hero path-trace validation remain required before GATED promotion.
