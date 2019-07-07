
# Interface

## Contextual

## Prioritized

## Logged

## Identifiable

## Locatable

## Versioned

# Services

## AbstractGateway

### AppService

App {about, prefs, quit, getVersion}

### CommandService[plugins]

future run(className, process, inputs)

CommandInfo
CommandModule

### ConsoleService[?]

### ConvertService

ConvertService{
    convert(src,dest);
    supports(src,dest);
    getCompatibleInputs(dest);
    getCompatibleInputClasses(dest);
    getCompatibleOutputClasses(src);
    }

Convert {
    canConvert(src, dest);
    convert(src, dest);
    convert(request);
    getOutputType();
    getInputType();
}

ConversionRequest{
    sourceClass();
    destClass();
}

### DisplayService

DisplayService{
    createDisplay(o)
    createDisplay(name, o);
    createDisplayQuielt(o);
    getActiveDisplay();
    getActiveDisplay(class);
    getDisplayPlugins();
    getDisplayPlugin(class);
    getDisplays();
    getDisplaysOfType(type);
}

### EventHistory

EventHistory{
    setActive()
    isActive()
    clear()
}

EventHistoryListener {
}

EventDetails{
}

### EventService

EventService{
    publish(e);
    publishLater(e);
    subscribe(o);
    unsubscribe(os);
    getSubscribers();
}

### IconService

{acquireDrawer(tool)}

### InputService

鼠标事件

InputService{
    is{Alt, AltGr, Ctrl, Meta, Shift}Down
    isKeyDown(key)
    getDisplay()
    getX()
    getY()
    isButtonDown()
}

### IOService

IOService : extends HandlerService<String, IOPlugin>{
    IOPlugin getOpener(source)
    IOPlugin getSaver(data, destination)
    open(source)
    save(data, destination)
}

IOPlugin : extends HandlerPlugin<String> {
    supportOpen(source)
    supportSave(destination)
    data open(source)
    save(data destination)
}

### LogService

LogService{
    setLevel()
}

### MainService

相当于Poco中的Application, 包含多个SubSystem
MainService {
    execMains()
}

### MenuService

（1）维护一个菜单结构体，在软件启动时加载插件后完成。
（2）利用上述结构体创建菜单树。在显示主界面之后完成

MenuService {
    getMenu()
}

## todo

### ModuleService

### ObjectService

### OptionsService

### PlatformService

### PluginService

### PrefSerce

### RecentFileService

### ScriptService

### StartupService

相当于启动画面

### StatusService

### TextService

### ThreadService

### ToolService

### UIService

### WidgetService

## Imagej

### AnimationService

### DataSetService

### ImageDisplayService

### LUTService

### NotebookService

### OpService

### OverlayService

### RenderService

### SamplerService

### ScreenCaptureService

### UpdateService

### UploaderService

### WindowService
```json
WindowService {
    add(displayName);
    remove(displayName);
    clear();
    getOpenWindows();
}
```
# Plugin

## RichPlugin

## SciJavaPlugin

## SingletonPlugin

## HandlerPlugin

## TypedPlugin

Interface for plugins with an associated type