import xml.etree.ElementTree as ET

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
    populated_slots_count = 0
    frequencies = []
    gpu_mem_int = int(data["gpu_memory"].text.strip())

    print("System Info:\n")
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

    for slot in data["memory_slots"]:
        capacity_element = slot.find('Capacity')
        if capacity_element is not None:
            capacity_value = float(capacity_element.find('DoubleValue').text)
            if capacity_value > 0:
                populated_slots_count += 1
                frequency_element = slot.find('Frequency')
                if frequency_element is not None:
                    frequency_value = float(frequency_element.find('DoubleValue').text) * 1000
                    frequencies.append(frequency_value)

    if data["memory_quantity"] is not None and data["memory_quantity"].text is not None:
        try:
            memory_int = int(data["memory_quantity"].text.strip())
            print("Memory:", memory_int // 1024, "GB (", memory_int // 1024 // populated_slots_count, "GB X",
                  populated_slots_count, ")")
        except ValueError:
            print("Memory: Could not convert to integer")
    else:
        print("Memory: Not found")
    print("Memory Frequency:", frequencies)

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

def parse_arielle_xml(arielle_xml_path):
    ari_tree = ET.parse(arielle_xml_path)
    ari_root = ari_tree.getroot()
    benchmark_test_name = ari_root.find('./sets/set/name')
    test_results = {result.find('name').text: float(result.find('value').text) for result in ari_root.findall('./results/result') if result.find('value') is not None}
    run_errors = ari_root.find('./sets/set/workloads/workload/results/result/status')

    if 'DandiaTestPassXST' in test_results:
        print("\nTest Passed!\nPass Summary List:" if test_results['DandiaTestPassXST'] == 1.0 else "\nTest Failed!\nFail Summary List:")
    else:
        print("DandiaTestPassXST not found. Cannot determine overall test result.")
    print("Test Case Name:", get_text(benchmark_test_name))

    if run_errors is not None:
        error_message = run_errors.text.strip() if run_errors.text else "Unknown error"
        print("\nErrors detected during the test run:", error_message)
    else:
        if 'DandiaLoopDoneXST' in test_results:
            print(
                f"Loops Completed (DandiaLoopDoneXST): {test_results['DandiaLoopDoneXST']} (Pass)" if test_results['DandiaLoopDoneXST'] >= 20 else f"Loops Completed (DandiaLoopDoneXST): {test_results['DandiaLoopDoneXST']} (Fail)")
        else:
            print("Loops Completed (DandiaLoopDoneXST) not found.")

        if 'DandiaFpsStabilityXST' in test_results:
            print(
                f"Frame Rate Stability (DandiaFpsStabilityXST): {test_results['DandiaFpsStabilityXST'] / 10}% (Pass)" if test_results['DandiaFpsStabilityXST'] >= 970.0 else f"Frame Rate Stability (DandiaFpsStabilityXST): {test_results['DandiaFpsStabilityXST'] / 10}% (Fail. Must be >= 97.0%)")
        else:
            print("Frame Rate Stability (DandiaFpsStabilityXST) not found.")

        fps_values = [(idx + 1, round(float(result.find('./primary_result').text), 2))
                      for idx, result in enumerate(ari_root.findall('.//result'))
                      if result.find('./primary_result') is not None and result.find('./primary_result').get('unit') == 'fps']

        print("\nIndividual FPS Values:")
        for idx, fps in fps_values:
            print(f"Loop {idx}: {fps} fps")

        if fps_values:
            average_fps = round(sum(fps for idx, fps in fps_values) / len(fps_values), 2)
            print(f"\nAverage FPS: {average_fps} fps")

            best_fps_idx, best_fps = max(fps_values, key=lambda x: x[1])
            worst_fps_idx, worst_fps = min(fps_values, key=lambda x: x[1])

            print(f"Best Individual Loop: Loop {best_fps_idx} with {best_fps} fps")
            print(f"Worst Individual Loop: Loop {worst_fps_idx} with {worst_fps} fps")
            margin = round(((best_fps / worst_fps) * 100 - 100), 2)
            print("Margin Between Best and Worst Runs:", f"{margin} %\n")
