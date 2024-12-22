import xml.etree.ElementTree as ET
import re
def get_text(element, default="Not found"):
    return element.text if element is not None else default

def calculate_difference(current, default, label):
    if current is not None and default is not None:
        diff = int(current.text) - int(default.text)
        status = "Overclocked" if diff > 0 else "Underclocked" if diff < 0 else "No Change"
        return f"\n{label} Difference: {diff} MHz ({status}) (Current: {current.text} MHz, Default: {default.text} MHz)"
    return f"\n{label} Difference: Not available"

def parse_si_xml(si_xml_path):
    si_tree = ET.parse(si_xml_path)
    si_root = si_tree.getroot()

    data = {
        "cpu_name": si_root.find('./Direct_Query_Info/CPU'),
        "monitor_name": si_root.find('.DirectX_Info/DXGI/Adapter/Output/DeviceString'),
        "monitor_res_width": si_root.find('.DirectX_Info/DXGI/Adapter/Output/PhysicalWidth'),
        "monitor_res_height": si_root.find('.DirectX_Info/DXGI/Adapter/Output/PhysicalHeight'),
        "gpu_card_name": si_root.find('./GPUZ_Info/GPUs/GPU/CARD_NAME'),
        "gpu_name": si_root.find('./GPUZ_Info/GPUs/GPU/GPU_NAME'),
        "gpu_memory": si_root.find('./GPUZ_Info/GPUs/GPU/MEM_SIZE'),
        "gpu_mem_type": si_root.find('./GPUZ_Info/GPUs/GPU/MEM_TYPE'),
        "gpu_driver_ver": si_root.find('./GPUZ_Info/GPUs/GPU/DRIVER_VER'),
        "gpu_driver_date": si_root.find('./GPUZ_Info/GPUs/GPU/DRIVER_DATE'),
        "gpu_driver_name": si_root.find('./GPUZ_Info/GPUs/GPU/DRIVER_NAME_NICE'),
        "gpu_mem_bus": si_root.find('./GPUZ_Info/GPUs/GPU/MEM_BUS_WIDTH'),
        "gpu_bandwidth": si_root.find('./GPUZ_Info/GPUs/GPU/MEM_BANDWIDTH'),
        "gpu_clock": si_root.find('./GPUZ_Info/GPUs/GPU/CLOCK_GPU'),
        "gpu_clock_default": si_root.find('./GPUZ_Info/GPUs/GPU/CLOCK_GPU_DEFAULT'),
        "gpu_mem_clock": si_root.find('./GPUZ_Info/GPUs/GPU/CLOCK_MEM'),
        "gpu_mem_clock_default": si_root.find('./GPUZ_Info/GPUs/GPU/CLOCK_MEM_DEFAULT'),
        "bus_interface_name": si_root.find('./GPUZ_Info/GPUs/GPU/BUS_INTERFACE_NAME_AND_SPEED'),
        "resize_bar": si_root.find('./GPUZ_Info/GPUs/GPU/RESIZABLE_BAR'),
        "os_ver": si_root.find('./Direct_Query_Info/OS'),
        "memory_quantity": si_root.find('./Direct_Query_Info/Memory'),
        "memory_slots": si_root.findall('.//Memory_Slot'),
        "motherboard_manufacturer": si_root.find('./Motherboard_Info/Manufacturer'),
        "motherboard_model": si_root.find('./Motherboard_Info/Model'),
        "motherboard_ver": si_root.find('./Motherboard_Info/Version'),
        "motherboard_bios_date": si_root.find('./Motherboard_Info/BIOS_Release_Date'),
        "version_elements": si_root.findall('./Motherboard_Info/Version')
    }

    # Initialize variables
    gpu_mem_int = int(data["gpu_memory"].text.strip())
    frequencies, populated_slots = parse_memory_info(data["memory_slots"])
    memory_total = int(data["memory_quantity"].text) // 1024 if data["memory_quantity"] is not None else "Not found"
    
    print("\nSystem Info:\n")
    print("Monitor (one used for the benchmark):", get_text(data["monitor_name"]))
    print("Monitor Resolution:", get_text(data["monitor_res_width"]), "X", get_text(data["monitor_res_height"]))
    print("\nCPU Name:", get_text(data["cpu_name"]))

    print("\nGPU Card Name:", get_text(data["gpu_card_name"]))
    print("GPU Name:", get_text(data["gpu_name"]))
    print("VRAM:", gpu_mem_int / 1024 if data["gpu_memory"] is not None else "Not found", "GB", get_text(data["gpu_mem_type"]))
    print("GPU Driver Name:", get_text(data["gpu_driver_name"]))
    print("GPU Driver Version:", get_text(data["gpu_driver_ver"]))
    print("GPU Driver Release Date:", get_text(data["gpu_driver_date"]))
    print("GPU Memory Bus:", get_text(data["gpu_mem_bus"]), "bits")
    print("GPU Bandwidth:", get_text(data["gpu_bandwidth"]),"GB/s")
    print("Resizable BAR:", get_text(data["resize_bar"]))
    print("Bus Interface:", get_text(data["bus_interface_name"]))
    print("\nOS:", get_text(data["os_ver"]))

    print(f"Memory: {memory_total/populated_slots} x {populated_slots} GB (Frequencies: {frequencies})")


    print("\nMotherboard Info: \n")
    print("Manufacturer:", get_text(data["motherboard_manufacturer"]))
    print("Model:", get_text(data["motherboard_model"]))
    print("Board Version:", get_text(data["motherboard_ver"]))

    if len(data["version_elements"]) > 1:
        specific_version = data["version_elements"][1].text
        print("BIOS Version:", specific_version)
    else:
        print("No second 'Version' element found.")

    print("BIOS Release Date:", get_text(data["motherboard_bios_date"]))

    print(calculate_difference(data["gpu_clock"], data["gpu_clock_default"], "GPU Clock"))
    print(calculate_difference(data["gpu_mem_clock"], data["gpu_mem_clock_default"], "GPU Memory Clock"))

def parse_memory_info(memory_slots):
    frequencies = [
        float(slot.find('Frequency/DoubleValue').text) * 1000
        for slot in memory_slots if slot.find('Capacity/DoubleValue') is not None
    ]
    populated_slots = len(frequencies)
    return frequencies, populated_slots

def extract_fps_values(ari_root):
    fps_values = [
        (idx + 1, round(float(result.find('./primary_result').text), 2))
        for idx, result in enumerate(ari_root.findall('.//result'))
        if result.find('./primary_result') is not None and result.find('./primary_result').get('unit') == 'fps'
    ]
    return fps_values
def check_benchmark_results_flexible(ari_root):
    # Define flexible patterns for the key result names
    test_pass_pattern = re.compile(r"DandiaTestPass.*")
    loops_completed_pattern = re.compile(r"DandiaLoopDone.*")
    fps_stability_pattern = re.compile(r"DandiaFpsStability.*")

    # Find matching elements
    test_pass = next((value for value in ari_root.findall(".//result") 
                      if value.find("name") is not None and test_pass_pattern.match(value.find("name").text)), None)
    loops_completed = next((value for value in ari_root.findall(".//result") 
                            if value.find("name") is not None and loops_completed_pattern.match(value.find("name").text)), None)
    fps_stability = next((value for value in ari_root.findall(".//result") 
                          if value.find("name") is not None and fps_stability_pattern.match(value.find("name").text)), None)

    # Extract values if matches are found
    if test_pass and loops_completed and fps_stability:
        test_pass_value = float(test_pass.find("value").text)
        loops_completed_value = float(loops_completed.find("value").text)
        fps_stability_value = float(fps_stability.find("value").text)

        # Validate the results
        if (
                test_pass_value == 1.0 and
                loops_completed_value == 20.0 and
                fps_stability_value > 97.0
            ):
                print("Pass")
                return True
        elif fps_stability_value < 97.0:
                print("Fail due to <97% FPS stability.")
                return False
        else:
            print("Fail due to incomplete test pass.")
            return False
    else:
        print("Error: Missing required result values in the XML.")
        return False
    
def parse_arielle_xml(arielle_xml_path):
    root = ET.parse(arielle_xml_path).getroot()
    fps_values = extract_fps_values(root)
    result = check_benchmark_results_flexible(root)
    print("\nBenchmark Result:", result)
    print("\nPerformance Metrics:")
    if fps_values:
        average_fps = round(sum(fps for _, fps in fps_values) / len(fps_values), 2)
        best_fps_idx, best_fps = max(fps_values, key=lambda x: x[1])
        worst_fps_idx, worst_fps = min(fps_values, key=lambda x: x[1])
        margin = round(((best_fps / worst_fps) * 100 - 100), 2)

        print(f"Average FPS: {average_fps} fps")
        print(f"Best FPS: Loop {best_fps_idx} with {best_fps} fps")
        print(f"Worst FPS: Loop {worst_fps_idx} with {worst_fps} fps")
        print(f"Performance Margin: {margin}%")
    else:
        print("No FPS data found.")
