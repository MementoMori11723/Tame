package main

import (
	"log/slog"
	"os"
	"strconv"
	"strings"

	rl "github.com/gen2brain/raylib-go/raylib"
)

const (
	title        = "Tame"
	screenWidth  = 1000
	screenHeight = 480
)

var (
	running = true

	bgColor = rl.NewColor(147, 211, 196, 255)

	grassSprite  rl.Texture2D
	hillSprite   rl.Texture2D
	fenceSprite  rl.Texture2D
	houseSprite  rl.Texture2D
	waterSprite  rl.Texture2D
	tilledSprite rl.Texture2D
	tex          rl.Texture2D

	playerSprite rl.Texture2D
	playerSrc    rl.Rectangle
	playerDest   rl.Rectangle

	playerUp, playerDown, playerLeft, playerRight bool

	playerMoving bool
	playerDir    int
	playerFrame  int
	frameCounter int

	tileDest   rl.Rectangle
	tileSrc    rl.Rectangle
	tileMap    []int
	srcMap     []string
	mapW, mapH int

	playerSpeed float32 = 1.5
	musicPaused bool
	music       rl.Music
	cam         rl.Camera2D
)

func drawScene() {
	for i := 0; i < len(tileMap); i++ {
		if tileMap[i] != 0 {
			tileDest.X = tileDest.Width * float32(i%mapW)
			tileDest.Y = tileDest.Height * float32(i/mapW)
			switch srcMap[i] {
			case "g":
				tex = grassSprite
			case "l":
				tex = hillSprite
			case "f":
				tex = fenceSprite
			case "h":
				tex = houseSprite
			case "w":
				tex = waterSprite
			case "t":
				tex = tilledSprite
			}
			tileSrc.X = tileSrc.Width * float32((tileMap[i]-1)%int(tex.Width/int32(tileSrc.Width)))
			tileSrc.Y = tileSrc.Height * float32((tileMap[i]-1)/int(tex.Width/int32(tileSrc.Width)))
			rl.DrawTexturePro(
				tex,
				tileSrc,
				tileDest,
				rl.NewVector2(tileDest.Width, tileDest.Height),
				0, rl.White,
			)
		}
	}

	rl.DrawTexturePro(
		playerSprite,
		playerSrc,
		playerDest,
		rl.NewVector2(playerDest.Width, playerDest.Height),
		0, rl.White,
	)
}

func input() {
	if rl.IsKeyDown(rl.KeyW) || rl.IsKeyDown(rl.KeyUp) {
		playerMoving = true
		playerDir = 1
		playerUp = true
	}

	if rl.IsKeyDown(rl.KeyS) || rl.IsKeyDown(rl.KeyDown) {
		playerMoving = true
		playerDir = 0
		playerDown = true
	}

	if rl.IsKeyDown(rl.KeyA) || rl.IsKeyDown(rl.KeyLeft) {
		playerMoving = true
		playerDir = 2
		playerLeft = true
	}

	if rl.IsKeyDown(rl.KeyD) || rl.IsKeyDown(rl.KeyRight) {
		playerMoving = true
		playerDir = 3
		playerRight = true
	}

	if rl.IsKeyPressed(rl.KeyM) {
		musicPaused = !musicPaused
	}
}

func update() {
	running = !rl.WindowShouldClose()

	playerSrc.X = playerSrc.Width * float32(playerFrame)
	if playerMoving {
		if playerUp {
			playerDest.Y -= playerSpeed
		}

		if playerDown {
			playerDest.Y += playerSpeed
		}

		if playerLeft {
			playerDest.X -= playerSpeed
		}

		if playerRight {
			playerDest.X += playerSpeed
		}

		if frameCounter%8 == 1 {
			playerFrame++
		} else if frameCounter%45 == 1 {
			playerFrame++
		}
	}

	frameCounter++

	if playerFrame > 3 {
		playerFrame = 0
	}

	if !playerMoving && playerFrame > 1 {
		playerFrame = 0
	}

	playerSrc.X = playerSrc.Width * float32(playerFrame)
	playerSrc.Y = playerSrc.Height * float32(playerDir)

	rl.UpdateMusicStream(music)
	if musicPaused {
		rl.PauseMusicStream(music)
	} else {
		rl.ResumeMusicStream(music)
	}

	cam.Target = rl.NewVector2(
		float32(playerDest.X-(playerDest.Width/2)),
		float32(playerDest.Y-(playerDest.Height/2)),
	)

	playerMoving = false
	playerUp, playerDown, playerLeft, playerRight = false, false, false, false
}

func render() {
	rl.BeginDrawing()
	rl.ClearBackground(bgColor)
	rl.BeginMode2D(cam)
	drawScene()
	rl.EndMode2D()
	rl.EndDrawing()
}

func loadMap(mapFile string) {
	file, err := os.ReadFile(mapFile)
	if err != nil {
		slog.Error(err.Error())
		os.Exit(1)
	}
	remNewLines := strings.Replace(string(file), "\n", " ", -1)
	sliced := strings.Split(remNewLines, " ")
	mapW = -1
	mapH = -1
	for i := 0; i < len(sliced); i++ {
		s, _ := strconv.ParseInt(sliced[i], 10, 64)
		m := int(s)
		if mapW == -1 {
			mapW = m
		} else if mapH == -1 {
			mapH = m
		} else if i < mapW*mapH+2 {
			tileMap = append(tileMap, m)
		} else {
			srcMap = append(srcMap, sliced[i])
		}
	}

	if len(tileMap) != mapW*mapH {
		tileMap = tileMap[:len(tileMap)-1]
	}
}

func init() {
	rl.InitWindow(screenWidth, screenHeight, title)
	rl.SetExitKey(rl.KeyEnd)
	rl.SetTargetFPS(60)

	grassSprite = rl.LoadTexture("assets/Tilesets/Grass.png")
	hillSprite = rl.LoadTexture("assets/Tilesets/Hills.png")
	fenceSprite = rl.LoadTexture("assets/Tilesets/Fences.png")
	houseSprite = rl.LoadTexture("assets/Tilesets/Wooden_House_Walls_Tilset.png")
	waterSprite = rl.LoadTexture("assets/Tilesets/Water.png")
	tilledSprite = rl.LoadTexture("assets/Tilesets/Tilled_Dirt.png")

	tileDest = rl.NewRectangle(0, 0, 16, 16)
	tileSrc = rl.NewRectangle(0, 0, 16, 16)

	playerSprite = rl.LoadTexture("assets/Characters/Basic Charakter Spritesheet.png")
	playerSrc = rl.NewRectangle(0, 0, 48, 48)
	playerDest = rl.NewRectangle(200, 200, 100, 100)
	rl.InitAudioDevice()
	music = rl.LoadMusicStream("assets/music/Avery's Farm.mp3")
	musicPaused = false
	rl.PlayMusicStream(music)
	cam = rl.NewCamera2D(
		rl.NewVector2(
			float32(screenWidth/2),
			float32(screenHeight/2),
		),
		rl.NewVector2(
			float32(playerDest.X-(playerDest.Width/2)),
			float32(playerDest.Y-(playerDest.Height/2)),
		),
		0.0, 2.7,
	)
	loadMap("assets/one.map")
}

func main() {
	for running {
		input()
		update()
		render()
	}
	quit()
}

func quit() {
	rl.UnloadTexture(grassSprite)
	rl.UnloadTexture(hillSprite)
	rl.UnloadTexture(fenceSprite)
	rl.UnloadTexture(houseSprite)
	rl.UnloadTexture(waterSprite)
	rl.UnloadTexture(tilledSprite)
	rl.UnloadTexture(playerSprite)
	rl.UnloadMusicStream(music)
	rl.CloseAudioDevice()
	rl.CloseWindow()
}
