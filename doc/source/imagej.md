
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

### ModuleService

At heart, a module is a {@link Runnable} piece of code, but with explicit typed input and output parameters.

插件的三种类型：Command, Tool, Display，其中的Command是一种Module，其他不是
 * A <em>module</em> is distinct from a <em>plugin</em> in that plugins extend
 * a program's functionality in some way, taking many forms, whereas modules
 * are always runnable code with typed inputs and outputs. There is a
 * particular type of plugin called a {@link org.scijava.command.Command} which
 * is also a module, but many plugins (e.g., {@link org.scijava.tool.Tool}s and
 * {@link org.scijava.display.Display}s) are not modules.

ModuleService{
    addModule(module)
    removeModule(module)
    getModuleById(id)
    createModule(info)
    future run(info, process, inputs)
    saveInputs(module)
    loadInputs(module)
}

Module : Runnable {
    preview()
    cancel()
    initialize()
    getInput()
    getOutput()
}

ModuleInfo

ModuleItem: metainfo about input or output of a module

DynamicCommand : DefaultMutableModule {
    a command with variable number of input and outputs
}

DefaultMutableModule : AbstractModule {

}

AbstractModule {
    
}

### ObjectService

ObjectService {
    addObject(obj)
    removeObject(obj)
}

### OptionsService

```json
OptionsService {
    getOption(cls) : get the options plugin of the given class, or None
}

OptionsPlugin: DynamicCommand{
和命令具有相同的接口，只不过不实际执行，而时将消息通过总线发送出去
}
```

```java
	@Override
	public void run() {
		save();
		eventService.publish(new OptionsEvent(this));
		resetState();
	}
```

### PlatformService

处理平台相关问题

### PluginService

PluginService {
    addPlugin(plugininfo);
    removePlugin(PluginInfo);
    getPlugins()
    getPluginsOfType(type);
    getPluginsofClass(cls)
}

PTService<PT> extends Service {
    a service for managing a particular sort of SciJavaPlugin
    plugin create(cls); //产生一种插件
}
### PrefService

保存任意配置

PrefService {
    get(cls, name)
    get(cls, name, defaultValue)
}

### RecentFileService

RecentFileService {
    add(path), remove(path), clear()
    getRecentFiles()
}

### ScriptService

### StartupService

相当于启动画面

### StatusService

StatusService {
    showProgress(value, maximum)
    showStatus()
    warn()
    clearStatus()
}

### TextService

TextService {
    open(file)
    asHtml(file)
    getHandler(file)
}

### ThreadService

管理一个线程池

ThreadService {
    queue(runable)
    future run(callable)
}

### ToolService

ToolService {
    Tool getTool(name)
    getActiveTool()
    setActiveTool(tool)
    reportRectangle()
    reportLine()
    reportPoint()
}

### UIService

把常用的界面操作收集到一起，便于普通代码与用户交互

UIService {
    addUI(ui)
    showUi(name)
    getDisplayViewer(display)
    show()
    showDialog(message)
    chooseFile()
    showContextMenu()
    getStatusMessage()
}

### WidgetService

由参数卡创建界面

WidgetService {
    createModule(inputPanel)
    getPluginType()
    getType()
}

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