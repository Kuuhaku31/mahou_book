
SOURCE = ./cpp/main.cpp

INCLUDES = ./cpp/

TARGET = copy_keyboard

BIN   = ./BIN
BUILD = ./BUILD

CXX = g++
CXXFLAGS = -std=c++11 -I$(INCLUDES)

all: $(TARGET)
$(TARGET): $(SOURCE)
	@mkdir -p $(BIN) $(BUILD)
	$(CXX) $(CXXFLAGS) -o $(BIN)/$(TARGET) $(SOURCE)

clean:
	@rm -rf $(BIN) $(BUILD)
	@echo "Cleaned up build files."