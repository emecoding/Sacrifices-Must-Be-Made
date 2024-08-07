class Animator:
    def __init__(self, frame_rate: float, frame_time: int):
        self.__mDefaultFrameRate: float = frame_rate
        self.__mCurrentFrameRate: float = frame_rate
        self.__mFrameTime: int = frame_time
        self.__mCurrentFrameTime: int = 0
        self.__mCurrentFrameIndex: int = 0

        self.__mAnimations: dict = {}

        self.__mCurrentAnimation: str = ""

        self.__mPlaying: bool = True

    def stop(self): self.__mPlaying = False

    def add_animation(self, name: str, frames: list, set_as_current_animation: bool = False):
        self.__mAnimations[name] = frames

        if set_as_current_animation:
            self.set_current_animation(name)

    def set_current_animation(self, animation: str):
        if self.__mCurrentAnimation == animation:
            return

        self.__mCurrentAnimation = animation
        self.__mCurrentFrameIndex = 0

    def set_frame_rate_for_one_animation(self, frame_rate: float):
        self.__mCurrentFrameRate = frame_rate

    def update_animations(self):
        if not self.__mPlaying:
            return

        self.__mCurrentFrameTime += self.__mCurrentFrameRate
        if self.__mCurrentFrameTime >= self.__mFrameTime:
            self.__mCurrentFrameTime = 0
            self.__mCurrentFrameIndex += 1
            if self.__mCurrentFrameIndex >= len(self.__mAnimations[self.__mCurrentAnimation]):
                self.__mCurrentFrameIndex = 0
                self.__mCurrentFrameRate = self.__mDefaultFrameRate

    def get_current_frame(self):
        return self.__mAnimations[self.__mCurrentAnimation][self.__mCurrentFrameIndex]

    def is_last_frame(self): return self.__mCurrentFrameIndex == len(self.__mAnimations[self.__mCurrentAnimation])-1

    def current_animation_name(self): return self.__mCurrentAnimation