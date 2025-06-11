
SOURCE = ./cpp/main.cpp

INCLUDES = ./cpp/

TARGET = copy_keyboard

BIN   = ./bin
BUILD = ./build

CXX = g++
CXXFLAGS += -I$(INCLUDES)

all: $(TARGET)
$(TARGET): $(SOURCE)
	@mkdir -p $(BIN) $(BUILD)
	$(CXX) $(CXXFLAGS) -o $(BIN)/$(TARGET) $(SOURCE)

run: all
	@echo "Running $(TARGET)"
	@echo "================================================"
	@$(BIN)/$(TARGET)

clean:
	@rm -rf $(BIN) $(BUILD)
	@echo "Cleaned up build files."

crun: clean run
