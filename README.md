# AGS Spin The Wheel
A spinning wheel written in Python for my school.

> [!WARNING]
> This program will only work on Windows!

### Credits
Winner sound effect by: https://safesearch.pixabay.com/users/freesound_community-46691455/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=6185

Wheel image by: https://pngtree.com/so/picmix-graphics-spin-wheel

Spin sound effect by: https://safesearch.pixabay.com/users/freesound_community-46691455/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=101152

Animated wheel by: https://safesearch.pixabay.com/users/mohamed_hassan-5229782/?utm_source=link-attribution&utm_medium=referral&utm_campaign=animation&utm_content=12315

### Building from source
1. Clone the repository:
```
git clone https://github.com/Gabriel-H189/AGSSpin
cd AGSSpin
```
2. Create a virtual environment:
```
python -m venv .venv
```
3. Activate virtual environment:
```
.venv\Scripts\activate.bat
```
5. Install prerequisites:
```
pip install pyinstaller
```
6. Run the build command:
```
pyinstaller main.pyw --onefile --add-data=wheel.png:wheel.png --add-data=win.wav:win.wav -n AGSSpin
```
7. Run:
```
dist\AGSSpin.exe
```
